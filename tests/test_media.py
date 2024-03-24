"""
This file contains tests for the media utility functions.
"""

import unittest
from vigi.utils.media import read_video_file_meta, generate_preview

class MediaTestCase(unittest.TestCase):
    """
    Test the media utility functions
    """
    def test_read_video_file_meta(self):
        """
        read_video_file_meta should return the correct metadata for a video file
        """
        meta = read_video_file_meta("tests/samples/positive/sample2.mov")
        self.assertEqual(meta["frame_width"], 1620)
        self.assertEqual(meta["frame_height"], 1080)
        self.assertEqual(meta["fps"], 30.0)
        self.assertEqual(meta["frame_count"], 331)
        self.assertEqual(meta["duration"], 11.0)

    def test_generate_preview(self):
        """
        preview should return the first frame of a video file
        """
        frame = generate_preview("tests/samples/positive/sample2.mov")
        self.assertIsNotNone(frame)
