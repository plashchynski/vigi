"""
This file contains the utility function to draw different figures using OpenCV
"""

import cv2
import numpy as np

def draw_bboxes(image, bboxes):
    """
    Draw bounding boxes on the image.
    """
    for bbox in bboxes:
        x1, y1, x2, y2 = bbox
        # select random color
        color = np.random.randint(0, 255, size=3).tolist()
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)

def draw_bbox(image, bbox, color=(255, 0, 255), label=None):
    """
    Draw a single bounding box on the image along with the label.
    """
    x1, y1, x2, y2 = bbox
    cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)

    if label:
        # display label
        cv2.putText(image, label, (int(x1-5), int(y1-5)), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

def draw_title(image, title, color=(0, 0, 255)):
    """
    Draw a title on the image.
    """
    cv2.putText(image, title, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
