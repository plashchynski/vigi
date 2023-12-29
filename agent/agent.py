from flask_bootstrap import Bootstrap5
from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)
bootstrap = Bootstrap5(app)

camera = cv2.VideoCapture(0)  # Use 0 for the first webcam

# generator function that yields frames
def generate_frames():
    while True:
        success, frame = camera.read()  # Read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
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
    app.run(host='0.0.0.0', port=8080)
