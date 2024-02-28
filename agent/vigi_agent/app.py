from datetime import datetime
import cv2
import numpy as np
from flask_bootstrap import Bootstrap5
from flask import Flask, Response, render_template, redirect, url_for

from .routes.live import live_blueprint

# Initialize the Flask app
app = Flask(__name__)

# Bootstrap wrapper for Flask
bootstrap = Bootstrap5(app)

def generate_frames():
    """Generate frames from the camera and send them to the client."""

    # For development, we can run flask without the camera monitor
    # because we don't have a camera connected to the development machine
    # and because we need to restart the server every time we change the code
    stream = None
    if hasattr(app, 'camera_monitor'):
        stream = app.camera_monitor.frame_stream.subscribe()

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
            app.camera_monitor.frame_stream.unsubscribe(stream)


# route for video streaming
@app.route('/camera')
def camera():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

app.register_blueprint(live_blueprint)

@app.route('/recordings')
def recordings():
    return render_template('recordings.html')

@app.route('/')
def index():
    return redirect(url_for('live.live'))
