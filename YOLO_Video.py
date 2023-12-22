from ultralytics import YOLO
import cv2
import math
# import mysql.connector
from geopy.geocoders import Nominatim

# MySQL Database Configuration
# db = mysql.connector.connect(
#     host="algojaxon.com",
#     user="drone",
#     password="u3F07n1!b",
#     database="drone"
# )
# cursor = db.cursor()

model = YOLO("best.pt")
classNames = ["crack"]
geolocator = Nominatim(user_agent="geo_locator")

DEFAULT_LATITUDE = 23.2499640
DEFAULT_LONGITUDE = 77.5228917

def get_current_location():
    try:
        # Replace with your IP address or leave it empty for automatic detection
        location = geolocator.geocode("0.0.0.0")

        if location:
            return f"{location.latitude}, {location.longitude}"
        else:
            return f"{DEFAULT_LATITUDE}, {DEFAULT_LONGITUDE}"
    except Exception as e:
        print(f"Error getting location: {e}")
        return f"{DEFAULT_LATITUDE}, {DEFAULT_LONGITUDE}"

def save_detection_to_database(class_name):
    location = get_current_location()
    query = "INSERT INTO detections (class_name,location) VALUES (%s,%s)"
    values = (class_name, location)
    cursor.execute(query, values)
    db.commit()
def video_detection(path_x):
    video_capture = path_x
    cap = cv2.VideoCapture(video_capture)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    detected_labels = []  # List to store detected labels

    while True:
        success, img = cap.read()
        if not success:
            break  # Exit the loop if no more frames

        results = model(img, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])
                class_name = classNames[cls]
                label = f'{class_name}{conf}'

                detected_labels.append(label)  # Add label to the list

                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                cv2.rectangle(img, (x1, y1), c2, [255, 0, 255], -1, cv2.LINE_AA)  # filled
                cv2.putText(img, label, (x1, y1 - 2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

    return img, detected_labels  # Return the image and detected labels

# You may want to add a proper exit condition for the video processing loop
# For example, add a break statement if a key is pressed or if the video ends

cv2.destroyAllWindows()

