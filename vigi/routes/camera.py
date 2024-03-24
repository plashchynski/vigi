"""
This module contains the camera routes blueprint.
"""

import cv2
import numpy as np

from flask import Blueprint, current_app, Response

camera_blueprint = Blueprint('camera', __name__)

def generate_frames(camera_monitor):
    """Generate frames from the camera and send them to the client."""

    # For development, we can run flask without the camera monitor
    # because we don't have a camera connected to the development machine
    # and because we need to restart the server every time we change the code
    stream = None
    if camera_monitor:
        stream = camera_monitor.frame_stream.subscribe()

    try:
        while True:
            # Get the frame from the stream
            if stream:
                frame = stream.get()
            else:
                # generate a black frame for the development environment
                frame = np.zeros((360, 640, 3), dtype=np.uint8)

                # Add no signal text
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, 'No signal', (50, 100), font, 2, (255, 255, 255), 2, cv2.LINE_AA)

            # Convert the frame to JPEG
            _ret, jpeg = cv2.imencode('.jpg', frame)

            # Convert the JPG to bytes
            frame_bytes = jpeg.tobytes()

            # Yield the frame to the client
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    except GeneratorExit:
        # If the client disconnects, unsubscribe from the stream
        if stream:
            camera_monitor.frame_stream.unsubscribe(stream)


# route for video streaming
@camera_blueprint.route('/camera/<camera_id>/live')
def camera(camera_id):
    """
    Returns the live video stream for the given camera_id.
    """
    camera_id = int(camera_id)
    camera_monitor = None
    if hasattr(current_app, 'camera_monitors'):
        camera_monitor = current_app.camera_monitors.get(camera_id)

        if camera_monitor is None:
            return Response("Camera monitor not found", status=404)

    return Response(generate_frames(camera_monitor),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
