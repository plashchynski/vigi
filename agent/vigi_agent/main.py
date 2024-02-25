import cv2
from flask_bootstrap import Bootstrap5
from flask import Flask, Response, render_template

from .motion_detector import MotionDetector

# Initialize the Flask app
app = Flask(__name__)

# Bootstrap wrapper for Flask
bootstrap = Bootstrap5(app)

# Initialize the camera with OpenCV
print("Starting camera... ", end="", flush=True)
camera = cv2.VideoCapture(0)  # Use 0 for the first webcam
print("done!", flush=True)

# This callback will be called when motion is detected
def motion_callback():
    print("Motion detected!")

print("Starting the motion detector... ", end="", flush=True)
motion_detector = MotionDetector(motion_callback)
print("done!", flush=True)

def generate_frames():
    """Generate frames from the camera and send them to the client."""
    while True:
        success, frame = camera.read()  # Read a frame from the camera
        if not success:
            print("Failed to read a frame from the camera")
            break

        else:
            # Apply the motion detector to the frame
            frame = motion_detector.update(frame)

            # Convert the frame to JPEG
            _ret, buffer = cv2.imencode('.jpg', frame)

            # Send the JPEG frame to the client
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # Concatenate frame with header

# route for video streaming
@app.route('/camera')
def video_stream():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# route for home page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
