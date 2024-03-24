# This is the entry point for the Flask application.

from flask_bootstrap import Bootstrap5
from flask import Flask, redirect, url_for

from .cache import cache
from .auth import auth
from .context_processors import utility_processor

from .routes.live import live_blueprint
from .routes.camera import camera_blueprint
from .routes.recordings import recordings_blueprint

# Initialize the Flask app
app = Flask(__name__, static_url_path='')

# setup the cache
cache.init_app(app)

# configure context processors for views
app.context_processor(utility_processor)

# Bootstrap wrapper for Flask
bootstrap = Bootstrap5(app)

# register the blueprints (sub-apps)
app.register_blueprint(live_blueprint)
app.register_blueprint(camera_blueprint)
app.register_blueprint(recordings_blueprint)

# configure the basic auth for all routes
@app.before_request
@auth.login_required
def before_request():
    pass

# the root route redirects to the live view
@app.route('/')
def index():
    return redirect(url_for('live.index'))
