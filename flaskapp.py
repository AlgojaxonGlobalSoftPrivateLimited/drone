from flask import Flask, render_template, Response, jsonify, request, session
from flask_wtf import FlaskForm
import secrets
from wtforms import FileField, SubmitField, StringField, DecimalRangeField, IntegerRangeField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired, NumberRange
import os
import cv2
import psycopg2  # Import the PostgreSQL connector

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# PostgreSQL Database Configuration
db_params = {
    "host": "dpg-cm2k3o6n7f5s73egch0g-a.oregon-postgres.render.com",
    "user": "drone",
    "password": "QQrJOIKv90lO3FvdT4sp6wDAkXNVOVy6",
    "dbname": "drone"
}

try:
    db = psycopg2.connect(**db_params)
except psycopg2.Error as e:
    print(f"Unable to connect to the database. Error: {e}")
    exit()

def generate_frames_web(path_x):
    # Your video_detection function here
    pass

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    session.clear()
    return render_template('indexproject.html')

# Other routes...

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

    # Pass the last "crack" detection to the template
    return render_template('ui.html', last_crack_detection=last_crack_detection)

# Other routes...

if __name__ == "__main__":
    app.run(debug=True, port=8082)
