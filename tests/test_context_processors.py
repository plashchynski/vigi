import unittest

from vigi.context_processors import utility_processor

class TestUtilityProcessor(unittest.TestCase):
    def setUp(self):
        self.utilities = utility_processor()

    def test_format_time(self):
        # Test that the format_time function returns the expected result as a time string
        self.assertEqual(self.utilities['format_time']("12-34-56"), "12:34:56")

    def test_format_duration_none(self):
        # Test the format_duration function should return "N/A" if the duration is None
        self.assertEqual(self.utilities['format_duration'](None), "N/A")

    def test_format_duration_seconds(self):
        # Test formatting of duration in seconds
        self.assertEqual(self.utilities['format_duration'](1), "1 second")
        self.assertEqual(self.utilities['format_duration'](2), "2 seconds")

        # Test formatting of duration in minutes (60 seconds)
        self.assertEqual(self.utilities['format_duration'](60), "1 minute")
