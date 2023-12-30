import cv2

class MotionDetector():
    def __init__(self, min_area = 500):
        self.fgbg = cv2.createBackgroundSubtractorMOG2(varThreshold=50)
        self.min_area = min_area

    def update(self, frame):
        original_frame = frame.copy()

        # Convert frame to grayscale and blur it
        blured_frame = cv2.GaussianBlur(frame, (21, 21), 0)
        fg_mask = self.fgbg.apply(blured_frame)

        # # Threshold the foreground mask to remove the shadows
        # _, fg_mask = cv2.threshold(fg_mask, 100, 255, cv2.THRESH_BINARY)

        # # Apply morphological operations to remove corruptions:
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        # fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, kernel, iterations=2)

        # # Find the contours of the detected objects:
        # contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # # Filter out the contours that are too small to be a car:
        # contours = [c for c in contours if cv2.contourArea(c) > self.min_area]

        # # Convex hull to get clean contours without holes:
        # contours = [cv2.convexHull(c) for c in contours]

        # # Prepare bounding boxes for the tracker
        # bboxes = []

        # # Get the bounding boxes of the contours:
        # for contour in contours:
        #     (x, y, w, h) = cv2.boundingRect(contour)

        #     bboxes.append([x, y, x+w, y+h])


        # for [x,y,x2,y2] in bboxes:
        #     # Draw the bounding box around the detected object
        #     cv2.rectangle(original_frame, (x, y), (x2, y2), (0, 255, 0), 1)

        return fg_mask
