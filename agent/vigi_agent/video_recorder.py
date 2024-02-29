import os
import time
import logging
import random

import cv2

DEFAULT_FPS = 25
DEFAULT_FRAME_WIDTH = 640
DEFAULT_FRAME_HEIGHT = 480

class VideoRecorder():
    """
    A class that records the video to a file.
    """
    def __init__(self, recording_path: str = "./recordings/"):
        self.recording = False
        self.recording_path = recording_path
        self.preview_saved = False
        self.time_str = None

    def start_recording(self, frame_width = None, frame_height = None, fps = None) -> None:
        """
        Start recording the video to a file.
        For each recording session, we pass the set of parameters (frame_width, frame_height, fps),
        as they can be changed between recording sessions.
        """

        if frame_width is None or frame_height is None:
            logging.error(f"Frame width and height were not provided. Set to default values of {DEFAULT_FRAME_WIDTH}x{DEFAULT_FRAME_HEIGHT}")
            frame_width = DEFAULT_FRAME_WIDTH
            frame_height = DEFAULT_FRAME_HEIGHT
            return

        if fps is None:
            logging.error(f"FPS was not provided. Set to default value of {DEFAULT_FPS}")
            fps = DEFAULT_FPS
            return

        self.recording = True
        self.preview_saved = False

        # ensure that the recording path exists
        # if not, create the directory
        if not os.path.exists(self.recording_path):
            logging.info(f"Creating directory: {self.recording_path}")
            os.makedirs(self.recording_path)
        
        # The recordings for each day will be saved in a separate directory
        # Ensure that the date path exists
        # if not, create the directory
        self.date_path = os.path.join(self.recording_path, time.strftime("%Y-%m-%d"))
        if not os.path.exists(self.date_path):
            logging.info(f"Creating directory: {self.date_path}")
            os.makedirs(self.date_path)

        self.time_str = time.strftime("%H-%M-%S")
        file_name = f"motion_detected_{self.time_str}.mp4"
        recording_full_path = os.path.join(self.date_path, file_name)
        logging.info(f"Recording video to: {recording_full_path}")

        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # For MP4 format
        self.video_writer = cv2.VideoWriter(
            filename = recording_full_path,
            fourcc = fourcc,
            fps = fps,
            frameSize = (int(frame_width), int(frame_height)),
        )

    def еnd_recording(self) -> None:
        """
        End the recording of the video to a file.
        """
        logging.info("Ending video recording...")
        self.recording = False
        self.video_writer.release()

    def is_recording(self) -> bool:
        """
        Returns True if the video is currently being recorded, otherwise False.
        """
        return self.recording

    def add_frame(self, frame) -> None:
        if self.recording:
            # Add the frame to the video file
            self.video_writer.write(frame)

            # save the first frame as a preview
            if not self.preview_saved:
                # Save the first frame as a preview
                preview_file_name = f"motion_detected_{self.time_str}.jpg"
                preview_path = os.path.join(self.date_path, preview_file_name)

                cv2.imwrite(preview_path, frame)
                self.preview_saved = True

            return
