import cv2
import numpy as np

camera = cv2.VideoCapture(0)

back_sub = cv2.createBackgroundSubtractorMOG2(varThreshold=100, detectShadows=True)

while True:
    success, original_frame = camera.read()  # Read a frame from the camera
    if not success:
        break

    # reduce the frame size to 50%
    original_frame = cv2.resize(original_frame, (0, 0), fx=0.5, fy=0.5)
    original_frame_img = original_frame.copy()
    # write the text "Original" on the frame
    cv2.putText(original_frame_img, "1. Original", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.rectangle(original_frame_img, (0, 0), (original_frame_img.shape[1], original_frame_img.shape[0]), (100, 100, 100), 2)

    gray_frame = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)
    gray_frame_img = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
    # write the text "Gray" on the frame
    cv2.putText(gray_frame_img, "2. Gray", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.rectangle(gray_frame_img, (0, 0), (gray_frame_img.shape[1], gray_frame_img.shape[0]), (100, 100, 100), 2)

    fg_mask = back_sub.apply(gray_frame)
    fg_mask_img = cv2.cvtColor(fg_mask, cv2.COLOR_GRAY2BGR)
    # write the text "Foreground Mask" on the frame
    cv2.putText(fg_mask_img, "3. Foreground Mask", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.rectangle(fg_mask_img, (0, 0), (fg_mask_img.shape[1], fg_mask_img.shape[0]), (100, 100, 100), 2)

    min_thresh = 100
    _result, motion_mask = cv2.threshold(fg_mask, thresh = min_thresh, maxval = 255, type = cv2.THRESH_BINARY)
    motion_mask_img = cv2.cvtColor(motion_mask, cv2.COLOR_GRAY2BGR)
    # write the text "Thresholded Motion Mask" on the frame
    cv2.putText(motion_mask_img, "4. Thresholded Motion Mask", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.rectangle(motion_mask_img, (0, 0), (motion_mask_img.shape[1], motion_mask_img.shape[0]), (100, 100, 100), 2)

    motion_mask_blured = cv2.medianBlur(motion_mask, ksize = 3)
    motion_mask_blured_img = cv2.cvtColor(motion_mask_blured, cv2.COLOR_GRAY2BGR)
    # write the text "Motion Mask Blured" on the frame
    cv2.putText(motion_mask_blured_img, "5. Motion Mask Blured", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.rectangle(motion_mask_blured_img, (0, 0), (motion_mask_blured_img.shape[1], motion_mask_blured_img.shape[0]), (100, 100, 100), 2)

    kernel = np.array((21,21), dtype=np.uint8)
    motion_mask_morph_open = cv2.morphologyEx(motion_mask_blured, op = cv2.MORPH_OPEN, kernel = kernel, iterations = 3)

    motion_mask_morph_close = cv2.morphologyEx(motion_mask_morph_open, op = cv2.MORPH_CLOSE, kernel = kernel, iterations = 3)
    motion_mask_morph_open_close_img = cv2.cvtColor(motion_mask_morph_close, cv2.COLOR_GRAY2BGR)
    # write the text "Motion Mask Morph Close" on the frame
    cv2.putText(motion_mask_morph_open_close_img, "6. MORPH_OPEN and MORPH_CLOSE", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.rectangle(motion_mask_morph_open_close_img, (0, 0), (motion_mask_morph_open_close_img.shape[1], motion_mask_morph_open_close_img.shape[0]), (100, 100, 100), 2)
    
    contours, _ = cv2.findContours(motion_mask_morph_close, mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_SIMPLE)
    # draw the contours on the black image
    contours_img = np.zeros_like(motion_mask_morph_open_close_img)
    cv2.drawContours(contours_img, contours, -1, (255, 255, 255), 2)
    # contours_img = cv2.cvtColor(contours_img, cv2.COLOR_GRAY2BGR)
    # write the text "Contours" on the frame
    cv2.putText(contours_img, "7. Contours", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.rectangle(contours_img, (0, 0), (contours_img.shape[1], contours_img.shape[0]), (100, 100, 100), 2)

    # filter by contour area
    cnt_area_thresh = 5000
    selected_countours = []
    detections = []
    for cnt in contours:
        
        area = cv2.contourArea(cnt)
        if area > cnt_area_thresh:
            x, y, w, h = cv2.boundingRect(cnt)
            selected_countours.append(cnt)
            detections.append([x, y, w, h])

    # draw the contours on the black image
    cv2.drawContours(contours_img, selected_countours, -1, (0, 0, 255), 2)
    # contours_img = cv2.cvtColor(contours_img, cv2.COLOR_GRAY2BGR)
    # write the text "Thresholded Contours" on the frame

    result_img = original_frame.copy()

    # bounding box
    for detection in detections:
        x, y, w, h = detection
        cv2.rectangle(result_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    cv2.putText(result_img, '8. Detections', (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # drow frame around the image
    cv2.rectangle(result_img, (0, 0), (result_img.shape[1], result_img.shape[0]), (100, 100, 100), 2)

    numpy_vertical = np.vstack((original_frame_img,
                                gray_frame_img,
                                fg_mask_img,
                                motion_mask_img))
    
    numpy_vertical2 = np.vstack((motion_mask_blured_img,
                                motion_mask_morph_open_close_img,
                                contours_img,
                                result_img))

    numpy_horizontal = np.hstack((numpy_vertical, numpy_vertical2))
    

    # show both the original and the gray frame
    cv2.imshow('motion detection steps', numpy_horizontal)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
