import unittest
from vigi_agent.utils.media import read_video_file_meta

class MediaTestCase(unittest.TestCase):
    def test_read_video_file_meta(self):
        # read_video_file_meta should return the correct metadata for a video file
        meta = read_video_file_meta("tests/samples/positive/sample2.mov")
        self.assertEqual(meta["frame_width"], 1620)
        self.assertEqual(meta["frame_height"], 1080)
        self.assertEqual(meta["fps"], 30.0)
        self.assertEqual(meta["frame_count"], 331)
        self.assertEqual(meta["duration"], 11.0)
