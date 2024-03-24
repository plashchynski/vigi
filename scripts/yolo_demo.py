"""
The purpose of this script is to test the YOLO model and OpenCV with the camera feed
outside of the main application code. This is useful for debugging and testing the YOLO model.

Usage:

    python yolo_demo.py

"""

import cv2
from ultralytics import YOLO

yolo = YOLO('yolov8n.pt')
camera = cv2.VideoCapture(0)

while True:
    success, frame = camera.read()  # Read a frame from the camera
    if not success:
        break

    results = yolo(frame)
    for result in results:
        for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
            label = result.names[int(cls)]
            x1, y1, x2, y2 = box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, label, (int(x1), int(y1)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
