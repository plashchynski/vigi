# This file is the entry point of the application. It reads the configuration file
# and the command line arguments, initializes the logger, the notifier, the video recorder
# and the camera monitor, and starts the Flask web server.

import os
import argparse
import logging
import configparser
import atexit
import urllib.request

from ultralytics import YOLO

from vigi.configuration_manager import ConfigurationManager

from vigi.notification_providers.email_notification_provider import EmailNotificationProvider
from vigi.notification_providers.sms_notification_provider import SMSNotificationProvider
from vigi.notifier import Notifier

from vigi.app import app
from vigi.video_recorder import VideoRecorder
from vigi.camera_monitor import CameraMonitor
from vigi.motion_detector import MotionDetector

from vigi.database import Database

DEFAULT_MODEL_URL = "https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8n.pt"

def read_args():
    """
    read the command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="Enable debug mode", action='store_true')
    parser.add_argument("--no-monitor", help="Disable the camera monitor", action='store_true')
    parser.add_argument("--data-dir", help="Directory to store the recordings", type=str)
    parser.add_argument("--camera-id", help="Camera ID to monitor", type=int)
    parser.add_argument("--host", help="Host to run the web server", type=str)
    parser.add_argument("--port", help="Port to run the web server", type=int)
    parser.add_argument("--max-errors", help="Maximum number of consecutive errors when reading a frame from the camera", type=int)
    parser.add_argument("--sensitivity", help="Sensitivity of the motion detector, should be a float between 0 and 1", type=float)
    parser.add_argument("--detection-model-file", help="Path to the detection model file (YOLO's yolov8n.pt, by default)", type=str)
    parser.add_argument("--disable-detection", help="Disable object detection", action='store_true')
    parser.add_argument("--inference-device", help="Inference device for object detection (cpu or cuda)", type=str)
    args = parser.parse_args()
    return args


def read_config():
    """
    Read the configuration file.
    """
    logging.info("Reading the configuration file... ")
    ini = configparser.ConfigParser()
    ini.read('vigi.ini')
    default = ini['DEFAULT']
    logging.info("Configuration file read successfully.")
    logging.debug(f"Default Configuration: {dict(default)}")

    camera_configs = []
    for section in ini.sections():
        # read the configuration from each camera
        if section.startswith('CAMERA'):
            camera_config = ini[section]
            logging.debug(f"Camera configuration: {dict(camera_config)}")
            camera_configs.append(camera_config)

    return default, camera_configs


def init_logger(debug):
    """
    Initialize the logger.
    """
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)


def init_notifier(configuration_manager):
    """
    Initialize the notifier and its notification providers.
    """
    logging.info("Initializing the notifier... ")
    notification_providers = []
    if configuration_manager.smtp_server_config:
        smtp_server_config = configuration_manager.smtp_server_config
        email_notification_provider = EmailNotificationProvider(
                smtp_server = smtp_server_config['smtpServer'],
                smtp_port = int(smtp_server_config['smtpPort']),
                smtp_user = smtp_server_config['smtpUser'],
                smtp_password = smtp_server_config['smtpPassword'],
                sender_email = smtp_server_config['senderEmail'],
                recipient_emails = smtp_server_config['recipientEmails']
            )
        notification_providers.append(email_notification_provider)

    if configuration_manager.twilio_config:
        twilio_config = configuration_manager.twilio_config
        sms_notification_provider = SMSNotificationProvider(
                account_sid = twilio_config['twilioAccountSid'],
                auth_token = twilio_config['twilioAuthToken'],
                from_number = twilio_config['twilioFromNumber'],
                recipient_phone_numbers = twilio_config['recipientPhoneNumbers']
            )
        notification_providers.append(sms_notification_provider)

    notifier = Notifier(notification_providers)
    logging.info("Notifier initialized successfully.")
    return notifier

def ensure_model_file() -> str:
    """
    Ensure that the detection model file exists by downloading it if it does not exist.
    return: str, the path to the detection model file
    """
    if app.configuration_manager.disable_detection:
        # we don't need the detection model file if the detection is disabled
        return None
    
    # check if the detection model file exists
    if os.path.exists(app.configuration_manager.detection_model_file):
        logging.info(f"Use detection model file: {app.configuration_manager.detection_model_file}")
    else:
        logging.info(f"Detection model file does not exist: {app.configuration_manager.detection_model_file}")
        # download the detection model file
        logging.info("Downloading the detection model file... ")
        urllib.request.urlretrieve(DEFAULT_MODEL_URL, app.configuration_manager.detection_model_file)
        logging.info("Detection model file downloaded successfully.")

    return app.configuration_manager.detection_model_file

def main():
    # Initialize the configuration with the default values
    app.configuration_manager = ConfigurationManager()

    # First, read the configuration file and update the configuration
    default_config, camera_configs = read_config()
    app.configuration_manager.update_from_config(default_config, camera_configs)

    # Then, read the command line arguments and update the configuration
    # the command line arguments take precedence over the configuration file
    args = read_args()
    app.configuration_manager.update_from_args(args)

    init_logger(app.configuration_manager.debug)

    # Check if the detection model file exists, download it if it does not exist
    object_detection_model_path = ensure_model_file()

    # create data dir if it does not exist
    if not os.path.exists(app.configuration_manager.data_dir):
        logging.info(f"Data directory does not exist, creating: {app.configuration_manager.data_dir}")
        os.makedirs(app.configuration_manager.data_dir)

    notifier = init_notifier(app.configuration_manager)

    logging.info("Initializing the database... ")
    database = Database(app.configuration_manager.db_path)
    database.init_db()
    database.integrity_check()

    # close the database connection after initializing the database 
    # as it's not used in the main thread
    database.close()

    logging.info("Database initialized successfully.")

    if app.configuration_manager.no_monitor:
        logging.info("Camera monitor is disabled.")
    else:
        app.camera_monitors = {}

        for camera_id, camera_config in app.configuration_manager.cameras_config.items():
            logging.info("Initializing the video recorder... ")
            video_recorder = VideoRecorder(
                recording_path = app.configuration_manager.data_dir,
                camera_id=camera_id
            )
            logging.info("Video recorder initialized successfully.")

            object_detection_model = None
            if object_detection_model_path:
                logging.info(f"Initializing the object detection model with YOLO weights {object_detection_model_path} on device {app.configuration_manager.inference_device}... ")
                object_detection_model = YOLO(object_detection_model_path)

            # create a motion detector for each camera
            motion_detector = MotionDetector(
                object_detection_model = object_detection_model,
                sensitivity = camera_config.sensitivity,
                inference_device = app.configuration_manager.inference_device
            )

            # create a camera monitor for each camera
            logging.info(f"Starting the camera monitor for camera {camera_id}... ")
            camera_monitor = CameraMonitor(
                video_recorder = video_recorder,
                camera_id = camera_id,
                max_errors = camera_config.max_errors,
                notifier = notifier,
                db_path = app.configuration_manager.db_path,
                motion_detector = motion_detector
            )
            camera_monitor.start()
            app.camera_monitors[camera_id] = camera_monitor
            logging.info(f"Camera monitor for camera {camera_id} started successfully.")

    def graceful_exit():
        logging.info("Exiting the application... ")
        if hasattr(app, 'camera_monitors'):
            for camera_monitor in app.camera_monitors.values():
                camera_monitor.stop()
        logging.info("Application exited successfully.")

    atexit.register(graceful_exit)

    logging.info("Starting the Flask web server... ")
    flask_debug = False
    if app.configuration_manager.debug and app.configuration_manager.no_monitor:
        # enable debug mode if the monitor is disabled, because
        # it cause race conditions in multithreading
        flask_debug = True
        logging.warning("Flask debug mode is enabled.")

    app.run(host=app.configuration_manager.host, port=app.configuration_manager.port, debug=flask_debug)
