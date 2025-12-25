import cv2
import pytz
import threading
import sys
import time
from io import BytesIO
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, time as time_type

import model_utils
import mongo_utils

# Debug: Log .env file path and contents
env_path = os.path.join(os.path.dirname(__file__), '.env')
print(f"Loading .env from: {env_path}")
if os.path.exists(env_path):
    with open(env_path, 'r') as f:
        print(f".env contents: {f.read()}")
else:
    print("Error: .env file not found")
load_dotenv(env_path)

TIME_ZONE = pytz.timezone('Asia/Kolkata')

TIME_SLOTS = [
   (time_type(7, 0), time_type(9, 0)),     # 8:00 AM - 9:00 AM
    (time_type(9, 00), time_type(10, 0)),   
    (time_type(10, 45), time_type(12, 00)),
    (time_type(12, 0), time_type(16, 0)),  
    (time_type(16, 0), time_type(20, 0)),   
    (time_type(23, 25), time_type(23, 59)),
    (time_type(20, 50), time_type(23, 59)),
    (time_type(1, 20), time_type(2, 0))     
]

def is_within_time_slots():
    """Check if current time is within any of the defined time slots."""
    current_time = datetime.now(TIME_ZONE).time()  
    for start_time, end_time in TIME_SLOTS:
        if start_time <= current_time <= end_time:
            return True
    return False

def check_frame(frame):
    try:
        res = model_utils.findSuspects(frame)
        found_suspect_ids = res['found_suspect_ids']
        suspects_img = res['suspects_img']

        num_suspects = len(found_suspect_ids)

        if num_suspects == 0:
            print('no match found')
            return

        print(num_suspects, 'matche(s) found')

        timestamp = time.strftime("%d/%m/%Y %H:%M:%S")

        print("At:", timestamp)
        print('\n--------found ids---------')
        print(found_suspect_ids)
        print('--------------------------\n')

        _, img_encoded = cv2.imencode('.jpg', suspects_img)
        img_bytes = img_encoded.tobytes()

        suspects_details = mongo_utils.getSuspectsDetails(found_suspect_ids)
        
        detection_records = []
        for suspect in suspects_details:
            caption = 'Student Name: {}\n Student Id: {}\n Branch: {}\n Found At: {}\n'.format(
                suspect['name'],
                suspect['studentId'],
                suspect['branch'],
                timestamp
            )
            print(caption)
            payload = {
                'name': suspect['name'],
                'studentId': suspect['studentId'],
                'branch': suspect['branch'],
                'timestamp': timestamp,
                'photoUrl': suspect['photoUrl']
            }
            detection_records.append({
                'studentId': suspect['studentId'],
                'name': suspect['name'],
                'branch': suspect['branch'],
                'timestamp': timestamp,
                'photoUrl': suspect['photoUrl']
            })
            recipient_email = os.getenv('RECIPIENT_EMAIL')
            if recipient_email:
                payload['to_email'] = recipient_email
                
            try:
                response = requests.post('http://localhost:5000/send-email', json=payload)
                print(f"POST to send-email: Status {response.status_code}, Response: {response.text}")
            except requests.RequestException as e:
                print(f"Failed to send POST to send-email: {str(e)}")

        # Store detection records
        if detection_records:
            mongo_utils.store_detection_records(detection_records)

    except Exception:
        pass

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

cap = cv2.VideoCapture(0)

# if using your webcam, comment the below two lines
# SOURCE_ADDRESS = 'YOUR CAMERAS IP ADDRESS'
# cap.open(SOURCE_ADDRESS)

if not cap.isOpened():
    print("Error opening camera")
    sys.exit()

cv2.namedWindow("Camera", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Camera", WINDOW_WIDTH, WINDOW_HEIGHT)

WAIT_DURATION = 4
FRAME_RATE = 30
target_frame = WAIT_DURATION * FRAME_RATE
frame_counter = 0

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error in reading frame from camera")
        break

    # Only process frame if within specified time slots
    if is_within_time_slots():
        if frame_counter % target_frame == 0:
            try:
                threading.Thread(target=check_frame, args=(frame.copy(),), daemon=True).start()
            except Exception as e:
                print(f'Error in creating new thread: {e}')
    else:
        print(f"Skipping detection: Current time {datetime.now(TIME_ZONE).time()} is outside detection time slots")

    frame_counter += 1

    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()