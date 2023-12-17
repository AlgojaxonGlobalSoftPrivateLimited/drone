from flask import Flask, render_template, Response,jsonify,request,session
from flask_wtf import FlaskForm
import secrets
from wtforms import FileField, SubmitField,StringField,DecimalRangeField,IntegerRangeField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired,NumberRange
import os
import cv2
from YOLO_Video import generate_frames_web

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    session.clear()
    return render_template('indexproject.html')

@app.route('/FrontPage', methods=['GET','POST'])
def frontpage():
    session.clear()
    return render_template('videoprojectnew.html')


@app.route("/webcam", methods=['GET','POST'])
def webcam():
    session.clear()
    return render_template('ui.html')


@app.route("/web", methods=['GET','POST'])
def web():
    session.clear()
    return render_template('web.html')



# To display the Output Video on Webcam page
@app.route('/webapp')
def webapp():
    rtsp_url = "rtsp://192.168.1.1/H264?W=720&H=400&FPS=30&BR=3000000/"
    return Response(generate_frames_web(rtsp_url), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True,port=8082)
