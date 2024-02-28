from flask_bootstrap import Bootstrap5
from flask import Flask, redirect, url_for

from .routes.live import live_blueprint
from .routes.camera import camera_blueprint
from .routes.recordings import recordings_blueprint

# Initialize the Flask app
app = Flask(__name__)

# Bootstrap wrapper for Flask
bootstrap = Bootstrap5(app)

app.register_blueprint(live_blueprint)
app.register_blueprint(camera_blueprint)
app.register_blueprint(recordings_blueprint)

@app.route('/')
def index():
    return redirect(url_for('live.live'))
