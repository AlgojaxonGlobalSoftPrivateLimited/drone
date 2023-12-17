from flask import Flask, render_template, Response, request
import secrets
from YOLO_Video import generate_frames_web

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('indexproject.html')

@app.route('/FrontPage', methods=['GET', 'POST'])
def frontpage():
    return render_template('videoprojectnew.html')

@app.route("/webcam", methods=['GET', 'POST'])
def webcam():
    return render_template('ui.html')

@app.route("/web", methods=['GET', 'POST'])
def web():
    return render_template('web.html')

# To display the Output Video on Webcam page
@app.route('/webapp', methods=['POST'])
def webapp():
    try:
        video_data = request.data
        return Response(generate_frames_web(video_data), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        return f'Error: {e}', 500

if __name__ == "__main__":
    app.run(debug=True, port=8082)
