from ultralytics import YOLO
import cv2
import math
import imutils

def video_detection(frame):
    model = YOLO("best.pt")
    classNames = ["crack"]

    frame = imutils.resize(frame, width=800)  # Resize the frame (adjust as needed)
    results = model(frame, stream=True)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # Display class label with confidence score
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            class_name = classNames[cls]
            label = f'{class_name}{conf}'
            t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
            c2 = x1 + t_size[0], y1 - t_size[1] - 3
            cv2.rectangle(frame, (x1, y1), c2, [255, 0, 255], -1, cv2.LINE_AA)  # filled
            cv2.putText(frame, label, (x1, y1 - 2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

    return frame

def generate_frames_web(rtsp_url):
    cap = cv2.VideoCapture(rtsp_url)

    while True:
        success, frame = cap.read()
        if not success:
            break

        detected_frame = video_detection(frame)

        _, buffer = cv2.imencode('.jpg', detected_frame)
        if buffer is not None:
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()
