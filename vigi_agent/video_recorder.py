import os
import time
import logging
import tempfile
import shutil

import cv2

DEFAULT_FPS = 25
DEFAULT_FRAME_WIDTH = 640
DEFAULT_FRAME_HEIGHT = 480

class VideoRecorder():
    """
    A class that records the video to a file.
    """
    def __init__(self, recording_path: str, camera_id: int):
        self.recording = False
        self.recording_path = recording_path
        self.camera_id = camera_id
        self.recording_full_path = None

    def start_recording(self, frame_width = None, frame_height = None, fps = None) -> None:
        """
        Start recording the video to a file.
        For each recording session, we pass the set of parameters (frame_width, frame_height, fps),
        as they can be changed between recording sessions.
        """

        logging.info("Starting video recording...")
        logging.info(f"Using parameters: Frame width: {frame_width}, frame height: {frame_height}, FPS: {fps}")

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
        self.recording_start_time = time.strftime("%H-%M-%S")
        self.recording_start_date = time.strftime("%Y-%m-%d")

        # save recording to a temporary directory
        self.recording_full_path = os.path.join(tempfile.gettempdir(), f"camera_{self.camera_id}.mp4")
        logging.info(f"Recording video to: {self.recording_full_path}")

        # fourcc = cv2.VideoWriter_fourcc(*'mp4v') # MPEG-4 Part 2 (Simple Profile) codec, doesn't work in Chrome
        fourcc = cv2.VideoWriter_fourcc(*'AVC1') # H.264 codec is not available on Apple M1, but 'AVC1' is the same as 'h264' and works in Chrome
        self.video_writer = cv2.VideoWriter(
            filename = self.recording_full_path,
            fourcc = fourcc,
            fps = int(fps),
            frameSize = (int(frame_width), int(frame_height)),
        )

    def еnd_recording(self) -> None:
        """
        End the recording of the video to a file.
        """
        logging.info("Ending video recording...")
        self.recording = False
        self.video_writer.release()

        # ensure that the recording path exists
        # if not, create the directory
        if not os.path.exists(self.recording_path):
            logging.info(f"Creating directory: {self.recording_path}")
            os.makedirs(self.recording_path)

        camera_id_path = os.path.join(self.recording_path, f"camera_{self.camera_id}")
        if not os.path.exists(camera_id_path):
            logging.info(f"Creating directory: {camera_id_path}")
            os.makedirs(camera_id_path)
        
        # The recordings for each day will be saved in a separate directory
        # Ensure that the date path exists
        # if not, create the directory
        date_path = os.path.join(camera_id_path, self.recording_start_date)
        if not os.path.exists(date_path):
            logging.info(f"Creating directory: {date_path}")
            os.makedirs(date_path)
        
        file_name = f"{self.recording_start_time}.mp4"

        complete_recording_path = os.path.join(date_path, file_name)

        logging.info(f"Moving the recording from {self.recording_full_path} to {complete_recording_path}")
        # move the recording from the temporary directory to the date directory
        shutil.move(self.recording_full_path, complete_recording_path)


    def is_recording(self) -> bool:
        """
        Returns True if the video is currently being recorded, otherwise False.
        """
        return self.recording

    def add_frame(self, frame) -> None:
        if self.recording:
            # Add the frame to the video file
            self.video_writer.write(frame)
            return
