"""
Test the FPS calculator
"""

import unittest
import time

from vigi.utils.fps_calculator import FPSCalculator

class TestFpsCalculator(unittest.TestCase):
    """
    Test the FPS calculator
    """
    def test_fps_calculator(self):
        """
        Test that the FPS calculator calculates the correct FPS
        """
        fps_calculator = FPSCalculator(max_history_size=50)

        for _ in range(100):
            fps_calculator.update()
            time.sleep(0.02)

        self.assertGreaterEqual(fps_calculator.current_fps(), 41)
        self.assertLessEqual(fps_calculator.current_fps(), 43)

    def test_fps_calculator_no_history(self):
        """
        current_fps should return None if the history is not long enough
        """
        fps_calculator = FPSCalculator(min_history_size=100)

        for _ in range(50):
            fps_calculator.update()
            time.sleep(0.01)

        self.assertIsNone(fps_calculator.current_fps())
