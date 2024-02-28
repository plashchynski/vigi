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
                frame = np.zeros((480, 640, 3), dtype=np.uint8)

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
@camera_blueprint.route('/camera')
def camera():
    camera_monitor = None
    if hasattr(current_app, 'camera_monitor'):
        camera_monitor = current_app.camera_monitor

    return Response(generate_frames(camera_monitor), mimetype='multipart/x-mixed-replace; boundary=frame')
