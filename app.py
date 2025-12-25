from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
import cv2
import numpy as np
from dotenv import load_dotenv
import cloudinary
from cloudinary.uploader import upload
from cloudinary.exceptions import Error as CloudinaryError
import os
import requests
from io import StringIO, BytesIO
import csv

import mongo_utils
import model_utils

# --------------------------------------------------
# Load environment variables
# --------------------------------------------------
env_path = os.path.join(os.path.dirname(__file__), '.env')
if not os.path.exists(env_path):
    raise RuntimeError(".env file not found")

load_dotenv(env_path)
print(".env loaded successfully")

# --------------------------------------------------
# Flask App
# --------------------------------------------------
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")

# --------------------------------------------------
# Cloudinary Configuration
# --------------------------------------------------
cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

# --------------------------------------------------
# Routes
# --------------------------------------------------

@app.route('/')
def index():
    students_list = list(
        mongo_utils.students_collection.find({}, {'_id': 0, 'embedding': 0})
    )
    return render_template('index.html', students_list=students_list)


@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'GET':
        return render_template('student_form.html', student=None)

    name = request.form['name']
    student_id = request.form['student_id']
    branch = request.form['branch']
    photo = request.files['photo']

    if photo.filename == '':
        flash('Empty photo file', 'error')
        return redirect(url_for('add_student'))

    try:
        upload_result = upload(photo)
        photo_url = upload_result['secure_url']

        photo.seek(0)
        img = cv2.imdecode(np.frombuffer(photo.read(), np.uint8), cv2.IMREAD_COLOR)
        embedding = model_utils.getEmbedding(img)

        if embedding is None:
            flash('Clear face not detected. Upload a better photo.', 'error')
            return redirect(url_for('add_student'))

        if mongo_utils.students_collection.find_one({'studentId': student_id}):
            flash('Student ID already exists.', 'error')
            return redirect(url_for('add_student'))

        mongo_utils.students_collection.insert_one({
            'name': name,
            'studentId': student_id,
            'branch': branch,
            'embedding': embedding,
            'photoUrl': photo_url
        })

        flash('Student added successfully', 'success')
        return redirect(url_for('index'))

    except CloudinaryError as e:
        flash(f'Cloudinary error: {e}', 'error')
        return redirect(url_for('add_student'))


@app.route('/edit-student/<student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = mongo_utils.getStudentDetails(student_id)

    if request.method == 'GET':
        return render_template('student_form.html', student=student)

    name = request.form['name']
    branch = request.form['branch']
    photo = request.files['photo']

    try:
        upload_result = upload(photo)
        photo_url = upload_result['secure_url']

        photo.seek(0)
        img = cv2.imdecode(np.frombuffer(photo.read(), np.uint8), cv2.IMREAD_COLOR)
        embedding = model_utils.getEmbedding(img)

        if embedding is None:
            flash('Clear face not detected.', 'error')
            return redirect(url_for('edit_student', student_id=student_id))

        mongo_utils.students_collection.update_one(
            {'studentId': student_id},
            {'$set': {
                'name': name,
                'branch': branch,
                'embedding': embedding,
                'photoUrl': photo_url
            }}
        )

        flash('Student updated successfully', 'success')
        return redirect(url_for('index'))

    except CloudinaryError as e:
        flash(f'Cloudinary error: {e}', 'error')
        return redirect(url_for('edit_student', student_id=student_id))


@app.route('/delete-student/<student_id>')
def delete_student(student_id):
    mongo_utils.deleteStudent(student_id)
    flash('Student removed successfully', 'success')
    return redirect(url_for('index'))


# --------------------------------------------------
# ✅ FIXED EMAILJS BACKEND (Supports Live Images)
# --------------------------------------------------
@app.route('/send-email', methods=['POST'])
def send_email():
    # Check if this is a file upload (live image) or just JSON
    live_image = request.files.get('live_image')
    
    if live_image:
        data = request.form  # When uploading files, data is in .form
    else:
        data = request.get_json() or {}

    if not data:
        return jsonify({'success': False, 'error': 'No data provided'})

    # Default to the database photo URL
    final_photo_url = data.get("photoUrl")

    # If a live captured image was sent, upload it to Cloudinary
    if live_image:
        try:
            print("Uploading live capture to Cloudinary...")
            upload_result = upload(live_image)
            final_photo_url = upload_result['secure_url']
            print(f"Live image uploaded: {final_photo_url}")
        except Exception as e:
            print(f"Cloudinary upload failed: {e}")
            # If upload fails, we keep 'final_photo_url' as the database photo (fallback)

    payload = {
        "service_id": os.getenv("EMAILJS_SERVICE_ID"),
        "template_id": os.getenv("EMAILJS_TEMPLATE_ID"),
        "user_id": os.getenv("EMAILJS_USER_ID"),         
        "accessToken": os.getenv("EMAILJS_PRIVATE_KEY"),  # REQUIRED for backend calls
        "template_params": {
            "to_name": data.get("name"),
            "student_id": data.get("studentId"),
            "branch": data.get("branch"),
            "timestamp": data.get("timestamp"),
            "photo_url": final_photo_url,  # This will be the live image URL if upload succeeded
            "to_email": os.getenv("RECIPIENT_EMAIL")
        }
    }

    try:
        response = requests.post(
            "https://api.emailjs.com/api/v1.0/email/send",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=10  # Increased timeout slightly for image upload time
        )

        if response.status_code != 200:
            print("EmailJS Error:", response.text)

        return jsonify({"success": response.status_code == 200})

    except requests.RequestException as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/download-report')
def download_report():
    detections = list(mongo_utils.detections_collection.find({}, {'_id': 0}))
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Name', 'Student ID', 'Branch', 'Timestamp', 'Photo URL'])

    for d in detections:
        writer.writerow([
            d['name'],
            d['studentId'],
            d['branch'],
            d['timestamp'],
            d['photoUrl']
        ])

    output.seek(0)
    return send_file(
        BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name='detection_report.csv'
    )


# --------------------------------------------------
# Main
# --------------------------------------------------
if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True)