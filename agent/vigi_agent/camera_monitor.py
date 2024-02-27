import sys
import threading
import time
import logging

import cv2

from .motion_detector import MotionDetector

from .pub_sub import PubSub


class CameraMonitor(threading.Thread):
    """
    A class that monitors the camera for motion and publishes the video stream from the camera.
    """

    def __init__(self, video_recorder = None, camera_id=0, max_errors=50):
        super().__init__()

        self.camera_id = camera_id
        self.max_errors = max_errors

        # Initialize the PubSub object to stream the frames from the camera
        # so other parts of the application can access the stream of frames
        self.frame_stream = PubSub()

        # Initialize the motion detector, when motion is detected, the motion_callback will be called
        self.motion_detector = MotionDetector(motion_callback=self.motion_callback)

        # video_recorder is used to save the video to a file when motion is detected
        self.video_recorder = video_recorder

    def motion_callback(self):
        logging.info("Motion detected!")
        self.video_recorder.start_recording(frame_width=self.frame_width, frame_height=self.frame_height, fps=self.fps)

    def run(self):
        # Initialize the camera with OpenCV
        logging.info("Starting camera monitor... ")
        camera = cv2.VideoCapture(self.camera_id)  # Use 0 for the first webcam
        if camera.isOpened():
            logging.info("Camera opened successfully.")
        else:
            logging.error(f"Camera with ID={self.camera_id} could not be opened.")
            return

        self.frame_width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.frame_height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.fps = camera.get(cv2.CAP_PROP_FPS)
        logging.info(f"Camera parameters: frame width: {self.frame_width}, frame height: {self.frame_height}, FPS: {self.fps}")

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
                if error_count >= self.max_errors:
                    logging.fatal(f"Maximum number of consecutive errors ({self.max_errors}) reached. Exiting.")
                    break

                logging.error(f"Failed to read a frame from the camera with ID={self.camera_id}")
                time.sleep(1)
                continue

            # Reset the error count if a frame is successfully read
            error_count = 0

            # Apply the motion detector to the frame
            frame = self.motion_detector.update(frame)

            # Publish the frame to the frame stream
            self.frame_stream.publish(frame)

            # if motion is not detected anymore and the video is being recorded, then stop the recording
            if not self.motion_detector.is_motion_detected() and self.video_recorder.is_recording():
                self.video_recorder.еnd_recording()

            # here we send all frames to the video recorder, it's up to the video recorder to decide if
            # it should record the frame or not. It could decide to record additional frames before and after
            # the motion is detected
            self.video_recorder.add_frame(frame)

        # OpenCV cleanup
        camera.release()
