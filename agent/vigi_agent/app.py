from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, redirect, url_for

from .routes.live import live_blueprint
from .routes.camera import camera_blueprint

# Initialize the Flask app
app = Flask(__name__)

# Bootstrap wrapper for Flask
bootstrap = Bootstrap5(app)

app.register_blueprint(live_blueprint)
app.register_blueprint(camera_blueprint)

@app.route('/recordings')
def recordings():
    return render_template('recordings.html')

@app.route('/')
def index():
    return redirect(url_for('live.live'))
