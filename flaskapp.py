from flask import Flask, render_template, Response,jsonify,request,session
from flask_wtf import FlaskForm
import secrets
from wtforms import FileField, SubmitField,StringField,DecimalRangeField,IntegerRangeField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired,NumberRange
import os
import cv2
from YOLO_Video import video_detection

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
# import mysql.connector
# MySQL Database Configuration
# db = mysql.connector.connect(
#    host="algojaxon.com",
#     user="drone",
#     password="u3F07n1!b",
#     database="drone"
# )

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
    # Perform object detection and get the image and detected labels
    img, detected_labels = video_detection(path_x=1)

    # Pass the detected labels to the template
    return render_template('ui.html', detected_labels=detected_labels)
    
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
