import sys
import logging
import configparser

logging.basicConfig(level=logging.INFO)

from vigi_agent.app import app
from vigi_agent.camera_monitor import CameraMonitor

logging.info("Reading the configuration file... ")
config = configparser.ConfigParser()
config.read('vigi.ini')
app.user_config = config['DEFAULT']
logging.info("Configuration file read successfully.")

if app.user_config['Debug'] == 'True':
    logging.getLogger().setLevel(logging.DEBUG)

logging.debug(f"Configuration: {dict(app.user_config)}")

logging.info("Starting the camera monitor... ")
camera_monitor = CameraMonitor(camera_id=int(app.user_config['CameraID']))
camera_monitor.start()
app.camera_monitor = camera_monitor
logging.info("Camera monitor started successfully.")

logging.info("Starting the Flask web server... ")
app.run(host='127.0.0.1', port=5000)
