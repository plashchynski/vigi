import logging
import configparser

logging.basicConfig(level=logging.INFO)

from vigi_agent.app import app
from vigi_agent.video_recorder import VideoRecorder
from vigi_agent.camera_monitor import CameraMonitor

logging.info("Reading the configuration file... ")
config = configparser.ConfigParser()
config.read('vigi.ini')
app.user_config = config['DEFAULT']
logging.info("Configuration file read successfully.")

if app.user_config['Debug'] == 'True':
    logging.getLogger().setLevel(logging.DEBUG)

logging.debug(f"Configuration: {dict(app.user_config)}")

logging.info("Initializing the video recorder... ")
video_recorder = VideoRecorder(recording_path = app.user_config['RecordingsPath'])
logging.info("Video recorder initialized successfully.")

logging.info("Starting the camera monitor... ")
camera_monitor = CameraMonitor(
        video_recorder = video_recorder,
        camera_id = int(app.user_config['CameraID']),
        max_errors = int(app.user_config['MaxErrors'])
    )
camera_monitor.start()
app.camera_monitor = camera_monitor
logging.info("Camera monitor started successfully.")

logging.info("Starting the Flask web server... ")
app.run(host='127.0.0.1', port=5000)
