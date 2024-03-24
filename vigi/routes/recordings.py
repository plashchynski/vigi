"""
This module contains the flask blueprint for the recordings page.
"""

import os
import logging
from pathlib import Path
from glob import glob

from flask import Blueprint, redirect, url_for, render_template, current_app, send_file, request
from vigi.utils.media import generate_preview, read_video_file_meta

from vigi.cache import cache
from vigi.database import Database

recordings_blueprint = Blueprint('recordings', __name__)

@recordings_blueprint.route('/recordings/<camera_id>/<date>/<time>/preview')
@cache.cached(timeout=24*60*60) # Cache the preview for 24 hours as it's a unlikely to change
def preview(camera_id, date, time):
    """
    Returns the preview image for the given camera_id, date and time
    """
    video_path = _video_file_path(camera_id, date, time)

    if not os.path.exists(video_path):
        return "Video not found", 404

    # get the path without the file extension
    video_preview_path = os.path.splitext(video_path)[0] + ".jpg"

    # check if a cached preview exists
    if os.path.exists(video_preview_path):
        # return the cached preview
        with open(video_preview_path, "rb") as f:
            return f.read(), 200, {'Content-Type': 'image/jpeg'}
    else:
        # generate a new preview
        jpg = generate_preview(video_path)

        if jpg is None:
            return(redirect(url_for('static', filename='no_preview_available.jpg')))

        return jpg, 200, {'Content-Type': 'image/jpeg'}


@recordings_blueprint.route('/recordings/<camera_id>/<date>/<time>/video')
def video(camera_id, date, time):
    """
    Returns the video file for the given camera_id, date and time
    """
    video_path = _video_file_path(camera_id, date, time)

    if not os.path.exists(video_path):
        return "Video not found", 404

    # if download=true is in the query string, the video will be downloaded
    as_attachment = request.args.get("download") == "true"

    return send_file(video_path, as_attachment=as_attachment)


# delete recording
@recordings_blueprint.route('/recordings/<camera_id>/<date>/<time>/delete', methods=['DELETE'])
def delete(camera_id, date, time):
    """
    Deletes the recording for the given camera_id, date and time
    """
    logging.info("Deleting recording: %s/%s/%s", camera_id, date, time)
    database = Database(current_app.configuration_manager.db_path)
    video_path = _video_file_path(camera_id, date, time)

    # delete video file
    if os.path.exists(video_path):
        os.remove(video_path)

    # delete meta data from database
    database.delete_recording(date, time, camera_id)
    database.close()

    # return 200
    return "", 200


@recordings_blueprint.route('/recordings')
def index():
    """
    Returns a list of all recordings
    """
    database = Database(current_app.configuration_manager.db_path)
    recording_path = current_app.configuration_manager.data_dir

    recordings = glob(os.path.join(recording_path, "**", "**", "*.mp4"))

    # check if recordings exist
    if len(recordings) == 0:
        return render_template('recordings/index.html', recording_dates=[])

    # get all unique recording dates from file names and sort them
    recording_dates = {os.path.basename(Path(file).parent) for file in recordings}
    recording_dates = list(recording_dates)
    recording_dates.sort(reverse=True)

    # for each file, get all relevant information and store it in a dictionary
    recordings = {}
    for recording_date in recording_dates:
        recordings[recording_date] = []

        for file in glob(os.path.join(recording_path, "**", recording_date, "*.mp4")):
            camera_id = Path(file).parent.parent.name.split("_")[1]
            time = Path(file).stem
            meta = read_video_file_meta(file)
            duration = 0
            if meta:
                duration = meta.get("duration")

            recording_info = {
                "time": time,
                "duration": duration,
                "camera_id": camera_id,
            }

            # find meta data for the recording in the database
            meta = database.find_recording(recording_date, time, camera_id)
            if meta:
                recording_info["tags"] = meta["tags"]

            recordings[recording_date].append(recording_info)

        # sort recordings by time
        recordings[recording_date].sort(key=lambda x: x["time"], reverse=True)

    database.close()

    return render_template('recordings/index.html',
                           recording_dates=recording_dates,
                           recordings=recordings)


def _video_file_path(camera_id, date, time):
    """
    Returns the absolute path to the video file for the given camera_id, date and time
    """
    recording_path = current_app.configuration_manager.data_dir
    camera_id_dir = f"camera_{camera_id}"
    return os.path.abspath(os.path.join(recording_path, camera_id_dir, date, f"{time}.mp4"))
