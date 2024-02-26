import sys
import threading
import time

import cv2

from .motion_detector import MotionDetector
from .pub_sub import PubSub


class CameraMonitor(threading.Thread):
    """
    A class that monitors the camera for motion and publishes the video stream from the camera.
    """

    def __init__(self, camera_id=0, max_consecutive_errors=50):
        super().__init__()

        self.camera_id = camera_id
        self.max_consecutive_errors = max_consecutive_errors

        # Initialize the PubSub object to stream the frames from the camera
        # so other parts of the application can access the stream of frames
        self.frame_stream = PubSub()

        # Initialize the motion detector, when motion is detected, the motion_callback will be called
        self.motion_detector = MotionDetector(motion_callback=self.motion_callback)

    def motion_callback(self):
        print("Motion detected!")

    def run(self):
        # Initialize the camera with OpenCV
        print("Starting camera... ", end="", flush=True)
        camera = cv2.VideoCapture(self.camera_id)  # Use 0 for the first webcam
        if camera.isOpened():
            print("done!", flush=True)
        else:
            print(f"Error: Camera with ID={self.camera_id} could not be opened.", file = sys.stderr)
            return

        error_count = 0
        while True:
            success, frame = camera.read()  # Read a frame from the camera
            if not success:
                # If the camera fails to read a frame:
                # - Increment the error count
                # - Print an error message
                # - Sleep for 1 second
                #
                # If the error count reaches the maximum number of consecutive errors:
                # - print an error message and break the loop

                error_count += 1
                if error_count >= self.max_consecutive_errors:
                    print(f"Error: Maximum number of consecutive errors ({self.max_consecutive_errors}) reached. Exiting.", file = sys.stderr)
                    break

                print(f"Error: Failed to read a frame from the camera with ID={self.camera_id}", file = sys.stderr)
                time.sleep(1)
                continue

            # Reset the error count if a frame is successfully read
            error_count = 0

            # Apply the motion detector to the frame
            frame = self.motion_detector.update(frame)

            # Publish the frame to the frame stream
            self.frame_stream.publish(frame)

        # OpenCV cleanup
        camera.release()
