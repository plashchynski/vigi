from queue import Queue

import cv2
import zmq
from flask_bootstrap import Bootstrap5
from flask import Flask, Response, render_template

# Initialize the Flask app
app = Flask(__name__)

# Bootstrap wrapper for Flask
bootstrap = Bootstrap5(app)

def generate_frames():
    """Generate frames from the camera and send them to the client."""
    stream = app.camera_monitor.frame_stream.subscribe()

    try:
        while True:
            if not stream.empty():
                # Get the frame from the stream
                frame = stream.get()

                # Convert the frame to JPEG
                _ret, jpeg = cv2.imencode('.jpg', frame)

                # Convert the JPG to bytes
                frame_bytes = jpeg.tobytes()

                # Yield the frame to the client
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    except GeneratorExit:
        # If the client disconnects, unsubscribe from the stream
        app.camera_monitor.frame_stream.unsubscribe(stream)


# route for video streaming
@app.route('/camera')
def video_stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# route for home page
@app.route('/')
def index():
    return render_template('index.html')
