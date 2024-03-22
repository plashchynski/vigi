# This file contains tests for the motion detector module and aims to verify that the motion detector
# is able to distinguish between videos that contain real motion and videos that do not contain any real motion

# The tests are based on sample videos that are located in the samples directory
# The samples directory contains two subdirectories: positive and negative
# The positive directory contains videos that contain real motion
# The negative directory contains videos that do not contain any real motion, but rather static scenes
# with some noise or light changes

import cv2
import os
from glob import glob
import unittest

from vigi.motion_detector import MotionDetector


class FileProcessor:
    """
    This class is responsible for processing video files and testing them for motion
    if motion is detected, the process method should return True, otherwise it should return False
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.motion_detected = False
    
    def motion_callback(self):
        self.motion_detected = True

    def process(self):
        cap = cv2.VideoCapture(self.file_path)

        motion_detector = MotionDetector(self.motion_callback)

        while True:
            # read frames from the sample video
            ret, frame = cap.read()
            if not ret: # end of video
                break

            motion_detector.update(frame)


class MotionDetectorTestCase(unittest.TestCase):
    def test_motion_detection(self):
        # negative samples are videos that do not contain any real motion, but rather static scenes
        # with some noise or light changes
        for file in glob(os.path.join(os.path.dirname(__file__), 'samples', 'negative', '*')):
            print(f"File {file} should not contain any motion.")
            processor = FileProcessor(file)
            processor.process()

            self.assertFalse(processor.motion_detected)

        # positive samples are videos that contain real motion
        for file in glob(os.path.join(os.path.dirname(__file__), 'samples', 'positive', '*')):
            print(f"File {file} should contain motion.")
            processor = FileProcessor(file)
            processor.process()

            self.assertTrue(processor.motion_detected)
