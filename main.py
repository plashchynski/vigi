# This file is the entry point of the application. It reads the configuration file
# and the command line arguments, initializes the logger, the notifier, the video recorder
# and the camera monitor, and starts the Flask web server.

import argparse
import logging
import configparser

from vigi_agent.agent_config import AgentConfig

from vigi_agent.notification_providers.email_notification_provider import EmailNotificationProvider
from vigi_agent.notification_providers.sms_notification_provider import SMSNotificationProvider
from vigi_agent.notifier import Notifier

from vigi_agent.app import app
from vigi_agent.video_recorder import VideoRecorder
from vigi_agent.camera_monitor import CameraMonitor




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

init_logger(app.agent_config.debug)

notifier = init_notifier(app.agent_config)

logging.info("Initializing the video recorder... ")
video_recorder = VideoRecorder(recording_path = app.agent_config.data_dir)
logging.info("Video recorder initialized successfully.")

if app.agent_config.no_monitor:
    logging.info("Camera monitor is disabled.")
else:
    logging.info("Starting the camera monitor... ")
    camera_monitor = CameraMonitor(
            video_recorder = video_recorder,
            camera_id = int(app.agent_config.camera_id),
            max_errors = int(app.agent_config.max_errors),
            notifier = notifier
        )
    camera_monitor.start()
    app.camera_monitor = camera_monitor
    logging.info("Camera monitor started successfully.")

logging.info("Starting the Flask web server... ")
app.run(host=app.agent_config.host, port=app.agent_config.port, debug=app.agent_config.debug)
