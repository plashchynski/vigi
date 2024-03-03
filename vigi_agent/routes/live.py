from datetime import datetime

from flask import Blueprint, current_app, render_template

live_blueprint = Blueprint('live', __name__)

# route for live
@live_blueprint.route('/live')
def index():
    if hasattr(current_app, 'camera_monitor'):
        camera_monitor = current_app.camera_monitor
        camera_id = camera_monitor.camera_id
        frame_width = camera_monitor.frame_width
        frame_height = camera_monitor.frame_height
        fps = camera_monitor.current_fps()
        start_time = camera_monitor.start_time
    else:
        # dummy values for the development environment
        camera_id = 0
        frame_width = 640
        frame_height = 480
        fps = 30
        start_time = datetime.now()

    return render_template('live/index.html', camera_id=camera_id, frame_width=frame_width,
                           frame_height=frame_height, fps=fps, start_time=start_time)
