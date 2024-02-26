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
    print("generate_frames called", flush=True)

    stream = app.camera_monitor.frame_stream.subscribe()

    while True:
        if not stream.empty():
            frame = stream.get()
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    app.camera_monitor.frame_stream.unsubscribe(stream)

# route for video streaming
@app.route('/camera')
def video_stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# route for home page
@app.route('/')
def index():
    return render_template('index.html')
