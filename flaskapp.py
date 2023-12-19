from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO, emit
import secrets
from YOLO_Video import generate_frames_web

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow all origins, adjust as needed


# The variable to store the latest video data
latest_video_data = None

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

# Sender: Route for setting up video stream
@app.route('/video_sender', methods=['POST'])
def video_sender():
    try:
        global latest_video_data
        video_data = request.data
        latest_video_data = video_data
        # Emit each frame to the 'receiver' room using WebSocket
        socketio.emit('frame', {'video_data': video_data}, room='receiver')
        return 'Video stream set up successfully'
    except Exception as e:
        return f'Error: {e}', 500

# Receiver: WebSocket route for receiving video stream
@socketio.on('connect', namespace='/receiver')
def handle_receiver_connect():
    global latest_video_data
    emit('frame', {'video_data': latest_video_data})

if __name__ == "__main__":
    socketio.run(app, debug=True, port=8082)
