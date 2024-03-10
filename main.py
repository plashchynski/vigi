# This file is the entry point of the application. It reads the configuration file
# and the command line arguments, initializes the logger, the notifier, the video recorder
# and the camera monitor, and starts the Flask web server.

import os
import argparse
import logging
import configparser
import atexit

from vigi_agent.agent_config import AgentConfig

from vigi_agent.notification_providers.email_notification_provider import EmailNotificationProvider
from vigi_agent.notification_providers.sms_notification_provider import SMSNotificationProvider
from vigi_agent.notifier import Notifier

from vigi_agent.app import app
from vigi_agent.video_recorder import VideoRecorder
from vigi_agent.camera_monitor import CameraMonitor

from vigi_agent.database import Database


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
    args = parser.parse_args()
    return args


def read_config():
    """
    Read the configuration file.
    """
    logging.info("Reading the configuration file... ")
    config = configparser.ConfigParser()
    config.read('vigi.ini')
    user_config = config['DEFAULT']
    logging.info("Configuration file read successfully.")

    if user_config['Debug'] == 'True':
        logging.getLogger().setLevel(logging.DEBUG)

    logging.debug(f"Configuration: {dict(user_config)}")

    return user_config


def init_logger(debug):
    """
    Initialize the logger.
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


def init_notifier(agent_config):
    """
    Initialize the notifier and its notification providers.
    """
    logging.info("Initializing the notifier... ")
    notification_providers = []
    if agent_config.smtp_server_config:
        smtp_server_config = agent_config.smtp_server_config
        email_notification_provider = EmailNotificationProvider(
                smtp_server = smtp_server_config['smtpServer'],
                smtp_port = int(smtp_server_config['smtpPort']),
                smtp_user = smtp_server_config['smtpUser'],
                smtp_password = smtp_server_config['smtpPassword'],
                sender_email = smtp_server_config['senderEmail'],
                recipient_emails = smtp_server_config['recipientEmails']
            )
        notification_providers.append(email_notification_provider)

    if agent_config.twilio_config:
        twilio_config = agent_config.twilio_config
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




# Initialize the configuration with the default values
app.agent_config = AgentConfig()

# First, read the configuration file and update the configuration
user_config = read_config()
app.agent_config.update_from_config(user_config)

# Then, read the command line arguments and update the configuration
# the command line arguments take precedence over the configuration file
args = read_args()
app.agent_config.update_from_args(args)

# create data dir if it does not exist
if not os.path.exists(app.agent_config.data_dir):
    logging.info(f"Data directory does not exist, creating: {app.agent_config.data_dir}")
    os.makedirs(app.agent_config.data_dir)

init_logger(app.agent_config.debug)

notifier = init_notifier(app.agent_config)

logging.info("Initializing the video recorder... ")
video_recorder = VideoRecorder(
        recording_path = app.agent_config.data_dir,
        camera_id=app.agent_config.camera_id
    )
logging.info("Video recorder initialized successfully.")

logging.info("Initializing the database... ")
database = Database(app.agent_config.db_path)
database.init_db()
database.integrity_check()

# close the database connection after initializing the database 
# as it's not used in the main thread
database.close()

logging.info("Database initialized successfully.")

if app.agent_config.no_monitor:
    logging.info("Camera monitor is disabled.")
else:
    logging.info("Starting the camera monitor... ")
    camera_monitor = CameraMonitor(
            video_recorder = video_recorder,
            camera_id = int(app.agent_config.camera_id),
            max_errors = int(app.agent_config.max_errors),
            notifier = notifier,
            db_path = app.agent_config.db_path,
            sensitivity=app.agent_config.sensitivity,
            debug=app.agent_config.debug
        )
    camera_monitor.start()
    app.camera_monitor = camera_monitor
    logging.info("Camera monitor started successfully.")

    video_recorder2 = VideoRecorder(
        recording_path = app.agent_config.data_dir,
        camera_id=1
    )

    # another camera monitor
    logging.info("Starting the second camera monitor... ")
    camera_monitor2 = CameraMonitor(
        video_recorder = video_recorder2,
        camera_id = 1,
        max_errors = int(app.agent_config.max_errors),
        notifier = notifier,
        db_path = app.agent_config.db_path,
        sensitivity=app.agent_config.sensitivity,
        debug=app.agent_config.debug
    )
    camera_monitor2.start()
    app.camera_monitor2 = camera_monitor2
    logging.info("Second camera monitor started successfully.")

def graceful_exit():
    logging.info("Exiting the application... ")
    if hasattr(app, 'camera_monitor'):
        app.camera_monitor.stop()

    if hasattr(app, 'camera_monitor2'):
        app.camera_monitor2.stop()

    logging.info("Application exited successfully.")

atexit.register(graceful_exit)

logging.info("Starting the Flask web server... ")
flask_debug = False
if app.agent_config.debug and app.agent_config.no_monitor:
    # enable debug mode if the monitor is disabled, because
    # it cause race conditions in multithreading
    flask_debug = True
    logging.warning("Flask debug mode is enabled.")

app.run(host=app.agent_config.host, port=app.agent_config.port, debug=flask_debug)
