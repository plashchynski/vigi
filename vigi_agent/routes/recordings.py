import os
import glob
from pathlib import Path

from flask import Blueprint, redirect, url_for, render_template, current_app, send_file
from vigi_agent.utils.media import generate_preview, read_video_file_meta

from vigi_agent.cache import cache

recordings_blueprint = Blueprint('recordings', __name__)

@recordings_blueprint.route('/recordings/<date>/<time>/preview')
@cache.cached(timeout=600) # Cache the preview for 10 minutes as it's a unlikely to change
def preview(date, time):
    video_path = video_file_path(date, time)

    # TODO: Check if video_path exists
    jpg = generate_preview(video_path)

    if jpg is None:
        return(redirect(url_for('static', filename='no_preview_available.jpg')))

    return jpg, 200, {'Content-Type': 'image/jpeg'}

@recordings_blueprint.route('/recordings/<date>/<time>/video')
def video(date, time):
    video_path = video_file_path(date, time)

    if not os.path.exists(video_path):
        return "Video not found", 404

    return send_file(video_path)


@recordings_blueprint.route('/recordings')
def index():
    recording_path = current_app.agent_config.data_dir

    # check if recording_path exists
    if not os.path.exists(recording_path):
        return render_template('recordings/index.html', recording_dates=[])

    # list dirs in recording path
    recording_dates = [
        entry for entry in os.listdir(recording_path)
        if os.path.isdir(os.path.join(recording_path, entry))
    ]

    # sort dates from newest to oldest
    recording_dates.sort(reverse=True)

    recordings = {}
    for recording_date in recording_dates:
        # list files in each directory
        directory = recording_date
        files = glob.glob(os.path.join(recording_path, directory, '*.mp4'))

        for file in files:
            meta_data = read_video_file_meta(file)
            if not meta_data:
                meta_data = {}

            # initialize the recordings dictionary
            recordings[recording_date] = recordings.get(recording_date, [])

            recordings[recording_date].append({
                "time": Path(file).stem,
                "duration": meta_data.get("duration"),
            })

            # sort recordings by time
            recordings[recording_date].sort(key=lambda x: x["time"], reverse=True)

    return render_template('recordings/index.html', recording_dates=recording_dates, recordings=recordings)

def video_file_path(date, time):
    recording_path = current_app.agent_config.data_dir
    return os.path.abspath(os.path.join(recording_path, date, f"{time}.mp4"))
