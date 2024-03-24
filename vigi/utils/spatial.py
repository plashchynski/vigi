"""
This module contains utility functions for spatial operations.
"""

import numpy as np

def boxes_intersect(box1, box2):
    """
    Check if two bounding boxes (box1 and box2) intersect with each other.
    Returns True if the boxes intersect, False otherwise.
    """

    # Unpack the coordinates
    b1_x1, b1_y1, b1_x2, b1_y2 = box1
    b2_x1, b2_y1, b2_x2, b2_y2 = box2

    # Check for overlap in both x and y axes
    overlap_x = np.minimum(b1_x2, b2_x2) - np.maximum(b1_x1, b2_x1) > 0
    overlap_y = np.minimum(b1_y2, b2_y2) - np.maximum(b1_y1, b2_y1) > 0

    return overlap_x and overlap_y
