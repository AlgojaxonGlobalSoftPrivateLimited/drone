from flask import Flask, render_template, Response, jsonify, request, session
from flask_wtf import FlaskForm
import secrets
from wtforms import FileField, SubmitField, StringField, DecimalRangeField, IntegerRangeField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired, NumberRange
import os
import cv2
import psycopg2  # Import the PostgreSQL connector
from YOLO_Video import video_detection 
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

import psycopg2
from urllib.parse import urlparse
url = urlparse("postgres://drone:QQrJOIKv90lO3FvdT4sp6wDAkXNVOVy6@dpg-cm2k3o6n7f5s73egch0g-a/drone")

# Extract connection parameters
db_params = {
    'host': "dpg-cm2k3o6n7f5s73egch0g-a.oregon-postgres.render.com",
    'user': url.username,
    'password': url.password,
    'database': url.path[1:],
}

try:
    db = psycopg2.connect(**db_params)
except psycopg2.Error as e:
    print(f"Unable to connect to the database. Error: {e}")
    exit()
def generate_frames_web(path_x):
    yolo_output = video_detection(path_x)
    for detection_ in yolo_output:
        ref,buffer=cv2.imencode('.jpg',detection_)

        frame=buffer.tobytes()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame +b'\r\n')
        

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    session.clear()
    return render_template('indexproject.html')

@app.route('/FrontPage', methods=['GET','POST'])
def frontpage():
    session.clear()
    return render_template('videoprojectnew.html')



@app.route("/webcam", methods=['GET', 'POST'])
def webcam():
    # Fetch the last "crack" detection from the database
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT class_name, timestamp_column FROM detections WHERE class_name='crack' ORDER BY timestamp_column DESC LIMIT 1")
            last_crack_detection = cursor.fetchone()
    except psycopg2.Error as e:
        db.rollback()  # Rollback the transaction in case of an error
        print(f"Error executing SQL query: {e}")
        last_crack_detection = None

    # Check if last_crack_detection is not None before accessing attributes
    if last_crack_detection:
        class_name, timestamp_column = last_crack_detection
        print(f"Last Crack Detection - Class: {class_name}, Timestamp: {timestamp_column}")
    else:
        print("No crack detections found.")

    # Pass the last "crack" detection to the template
    return render_template('ui.html', last_crack_detection=last_crack_detection)


@app.route("/web", methods=['GET','POST'])
def web():
    session.clear()
    return render_template('web.html')


@app.route('/chart', methods=['GET','POST'])
def chart():
    session.clear()
    return render_template('chart.html')

# To display the Output Video on Webcam page
@app.route('/webapp')
def webapp():
    #return Response(generate_frames(path_x = session.get('video_path', None),conf_=round(float(session.get('conf_', None))/100,2)),mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(generate_frames_web(path_x=1), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True,port=8082)
