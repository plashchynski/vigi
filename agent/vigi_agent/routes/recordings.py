import os
import glob
from pathlib import Path

from flask import Blueprint, redirect, url_for, render_template, current_app
from vigi_agent.utils.media import generate_preview

from vigi_agent.cache import cache

recordings_blueprint = Blueprint('recordings', __name__)

@recordings_blueprint.route('/recordings/<date>/<time>/preview')
@cache.cached(timeout=600) # Cache the preview for 10 minutes as it's a unlikely to change
def preview(date, time):
    recording_path = "recordings/"
    video_path = os.path.join(recording_path, date, f"{time}.mp4")
    jpg = generate_preview(video_path)

    if jpg is None:
        return(redirect(url_for('static', filename='no_preview_available.jpg')))

    return jpg, 200, {'Content-Type': 'image/jpeg'}

@recordings_blueprint.route('/recordings')
def index():
    # recording_path = current_app.user_config['RecordingsPath']
    recording_path = "recordings/"

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

        # basename the files
        recordings[directory] = [
            {
                "time": Path(file).stem
            }
            for file in files
        ]

    return render_template('recordings/index.html', recording_dates=recording_dates, recordings=recordings)
