"""
This module contains tests for the spatial utility functions in vigi.utils.spatial.
"""

import unittest
from vigi.utils.spatial import boxes_intersect

class SpatialTestCase(unittest.TestCase):
    """
    Test the spatial utility functions
    """
    def test_boxes_intersect(self):
        """
        boxes_intersect should return True if two boxes intersect
        """
        self.assertTrue(boxes_intersect((0, 0, 2, 2), (1, 1, 3, 3)))

    def test_boxes_do_not_intersect(self):
        """
        boxes_intersect should return False if two boxes do not intersect
        """
        self.assertFalse(boxes_intersect((0, 0, 1, 1), (2, 2, 3, 3)))
