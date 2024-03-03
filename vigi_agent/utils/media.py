# This module contains utility functions for working with media files.

import cv2
import random

def read_video_file_meta(video_path):
    """
    Read the metadata of a video file and return it as a dictionary.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = int(frame_count / fps)

    cap.release()

    return {
        "frame_width": frame_width,
        "frame_height": frame_height,
        "fps": fps,
        "frame_count": frame_count,
        "duration": duration
    }

def generate_preview(video_path):
    """
    Open video file, select a random frame and return it as a JPEG image for preview.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return None
    
    # get the total number of frames in the video
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # select random frame to start preview
    frame_number = int(frame_count * random.random())

    # select the frame for the preview
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    # read the frame
    ret, frame = cap.read()
    if not ret:
        return None
    
    cap.release()

    # convert the frame to JPEG and return it
    _, frame = cv2.imencode('.jpg', frame)

    return frame.tobytes()
