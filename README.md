CampusEye: Next-Gen Intelligent Surveillance System
===================================================

CampusEye is an advanced real-time surveillance and attendance management system that leverages face recognition technology to identify registered students, log their presence, and send automated alerts to administrators.

🚀 Key Features
---------------

*   **Real-time Face Recognition**: Utilizes the DeepFace library with Facenet to detect and identify faces from a live camera feed.
    
*   **Student Management Dashboard**: A web-based interface built with Flask to add, edit, and delete student profiles.
    
*   **Automated Alerts**: Sends instant email notifications with live captures of detected students via EmailJS.
    
*   **Attendance Logging**: Automatically records student presence in a local attendance.csv file and a MongoDB database.
    
*   **Report Generation**: Export detection records and attendance logs as CSV reports directly from the dashboard.
    
*   **Time-Slot Monitoring**: Surveillance logic can be configured to run only during specific designated hours.
    

🛠️ Technology Stack
--------------------

*   **Backend**: Python, Flask
    
*   **Database**: MongoDB (PyMongo)
    
*   **Computer Vision**: OpenCV, DeepFace (Facenet)
    
*   **Cloud Storage**: Cloudinary (for storing student photographs)
    
*   **Email Service**: EmailJS
    
*   **Frontend**: HTML5, CSS3
    

📋 Prerequisites
----------------

Before you begin, ensure you have the following accounts and credentials:

*   **Python 3.8+**
    
*   **MongoDB Atlas**: A connection URI for your database.
    
*   **Cloudinary**: Cloud name, API key, and API secret.
    
*   **EmailJS**: Service ID, Template ID, User ID, and Private Key.
    

⚙️ Installation
---------------

### 1\. Clone the Repository

Bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   git clone   cd CampusEye   `

### 2\. Create a Virtual Environment

Bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python -m venv venv  # On Windows  venv\Scripts\activate  # On macOS/Linux  source venv/bin/activate   `

### 3\. Install Dependencies

Bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   pip install -r requirements.txt   `

The project requires several libraries including Flask, deepface, opencv-python, pymongo, and cloudinary.

### 4\. Configure Environment Variables

Create a .env file in the root directory and add the following keys:

Code snippet

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   # Flask  FLASK_SECRET_KEY=your_secret_key  # MongoDB  MONGODB_URI=your_mongodb_connection_string  # Cloudinary  CLOUD_NAME=your_cloud_name  API_KEY=your_api_key  API_SECRET=your_api_secret  # EmailJS  EMAILJS_SERVICE_ID=your_service_id  EMAILJS_TEMPLATE_ID=your_template_id  EMAILJS_USER_ID=your_user_id  EMAILJS_PRIVATE_KEY=your_private_key  RECIPIENT_EMAIL=admin@example.com  # Telegram (Optional)  BOT_TOKEN=your_bot_token  CHAT_ID=your_chat_id   `

🏃 Running the Application
--------------------------

### 1\. Start the Web Dashboard

Launch the Flask server to manage student registrations:

Bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python app.py   `

Access the dashboard at http://127.0.0.1:5000.

### 2\. Launch the Surveillance System

Run the main script to start real-time monitoring via your camera:

Bash

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   python main.py   `

_Note: Press 'q' to stop the camera feed._

📁 Project Structure
--------------------

*   app.py: Flask application for student management and report downloads.
    
*   main.py: The core surveillance script handling camera feed and detection logic.
    
*   model\_utils.py: Face embedding and representation utilities using DeepFace.
    
*   mongo\_utils.py: Database operations for MongoDB.
    
*   attendance.csv: Local log for recording student attendance timestamps.
    
*   templates/: HTML templates for the dashboard UI.
    
*   static/: CSS and image assets.
    

👥 Contributors
---------------

This project was developed by:

*   Reshmitha
    
*   Pavan
    
*   Yaswanth
    
*   Govind