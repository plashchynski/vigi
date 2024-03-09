import os
from pathlib import Path
from glob import glob

from flask import Blueprint, redirect, url_for, render_template, current_app, send_file
from vigi_agent.utils.media import generate_preview, read_video_file_meta

from vigi_agent.cache import cache

recordings_blueprint = Blueprint('recordings', __name__)

@recordings_blueprint.route('/recordings/<camera_id>/<date>/<time>/preview')
@cache.cached(timeout=600) # Cache the preview for 10 minutes as it's a unlikely to change
def preview(camera_id, date, time):
    video_path = video_file_path(camera_id, date, time)

    # TODO: Check if video_path exists
    jpg = generate_preview(video_path)

    if jpg is None:
        return(redirect(url_for('static', filename='no_preview_available.jpg')))

    return jpg, 200, {'Content-Type': 'image/jpeg'}

@recordings_blueprint.route('/recordings/<camera_id>/<date>/<time>/video')
def video(camera_id, date, time):
    video_path = video_file_path(camera_id, date, time)

    if not os.path.exists(video_path):
        return "Video not found", 404

    return send_file(video_path)


@recordings_blueprint.route('/recordings')
def index():
    recording_path = current_app.agent_config.data_dir

    recordings = glob(os.path.join(recording_path, "**", "**", "*.mp4"))

    # check if recordings exist
    if len(recordings) == 0:
        return render_template('recordings/index.html', recording_dates=[])

    recording_dates = set([os.path.basename(Path(file).parent) for file in recordings])
    recording_dates = list(recording_dates)
    recording_dates.sort(reverse=True)

    recordings = {}
    for recording_date in recording_dates:
        recordings[recording_date] = [
            {
                "time": Path(file).stem,
                "duration": read_video_file_meta(file).get("duration"),
                "camera_id": Path(file).parent.parent.name.split("_")[1],
            }
            for file in glob(os.path.join(recording_path, "**", recording_date, "*.mp4"))
        ]
        recordings[recording_date].sort(key=lambda x: x["time"], reverse=True)

    return render_template('recordings/index.html', recording_dates=recording_dates, recordings=recordings)

def video_file_path(camera_id, date, time):
    recording_path = current_app.agent_config.data_dir
    camera_id_dir = f"camera_{camera_id}"
    return os.path.abspath(os.path.join(recording_path, camera_id_dir, date, f"{time}.mp4"))
