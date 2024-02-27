# The purpose of this script is to test the YOLO model and OpenCV with the camera feed
# outside of the main application code. This is useful for debugging and testing the YOLO model.

import threading
import cv2
from ultralytics import YOLO

class Test(threading.Thread):
    def __init__(self):
        super().__init__()
        self.yolo = YOLO('yolov8n.pt')

    def run(self):
        camera = cv2.VideoCapture(0)

        error_count = 0
        max_errors = 50

        while True:
            success, frame = camera.read()  # Read a frame from the camera
            if success:
                error_count = 0

                results = self.yolo(frame)
                for result in results:
                    for box, cls in zip(result.boxes.xyxy, result.boxes.cls):
                        label = result.names[int(cls)]
                        x1, y1, x2, y2 = box
                        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

                # cv2.imshow('frame', frame)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break
            else:
                error_count += 1
                if error_count > max_errors:
                    print("Too many errors. Exiting...")
                    break

        camera.release()
        cv2.destroyAllWindows()

thread = Test()
thread.start()
thread.join()
