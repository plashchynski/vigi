import argparse
import logging
import configparser

from platformdirs import user_data_dir

from vigi_agent.notification_providers.email_notification_provider import EmailNotificationProvider
from vigi_agent.notification_providers.sms_notification_provider import SMSNotificationProvider
from vigi_agent.notifier import Notifier

from vigi_agent.app import app
from vigi_agent.video_recorder import VideoRecorder
from vigi_agent.camera_monitor import CameraMonitor




def init_args():
    """
    read the command line arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", help="Enable debug mode", action='store_true')
    parser.add_argument("--no-monitor", help="Disable the camera monitor", action='store_true')
    parser.add_argument("--data-dir", help="Directory to store the recordings", type=str)
    parser.add_argument("--host", help="Host to run the web server", type=str, default='localhost')
    parser.add_argument("--port", help="Port to run the web server", type=int, default=5000)
    args = parser.parse_args()
    return args


def init_logger(debug):
    """
    Initialize the logger.
    """
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


def init_datadir(app, args):
    """
    Initialize the data directory.
    """
    logging.info("Initializing the data directory... ")
    data_dir = None
    if app.user_config.get('RecordingsPath'):
        data_dir = app.user_config['RecordingsPath']
    elif args.data_dir:
        data_dir = args.data_dir
    else:
        data_dir = user_data_dir('vigi-agent', 'Vigi')
        logging.warning(f"RecordingsPath is not set in the configuration file. Using the default path: {data_dir}")

    app.data_dir = data_dir
    logging.info(f"Recordings will be stored in: {data_dir}")


def init_notifier(app):
    """
    Initialize the notifier and its notification providers.
    """
    logging.info("Initializing the notifier... ")
    notification_providers = []
    if app.user_config.get('smtpServer'):
        email_notification_provider = EmailNotificationProvider(
                smtp_server = app.user_config['smtpServer'],
                smtp_port = int(app.user_config['smtpPort']),
                smtp_user = app.user_config['smtpUser'],
                smtp_password = app.user_config['smtpPassword'],
                sender_email = app.user_config['senderEmail'],
                recipient_emails = app.user_config['recipientEmails'].split(',')
            )
        notification_providers.append(email_notification_provider)

    if app.user_config.get('twilioAccountSid'):
        sms_notification_provider = SMSNotificationProvider(
                account_sid = app.user_config['twilioAccountSid'],
                auth_token = app.user_config['twilioAuthToken'],
                from_number = app.user_config['twilioFromNumber'],
                recipient_phone_numbers = app.user_config['recipientPhoneNumbers'].split(',')
            )
        notification_providers.append(sms_notification_provider)

    app.notifier = Notifier(notification_providers)
    logging.info("Notifier initialized successfully.")


def init_config():
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

args = init_args()

init_logger(args.debug)

app.user_config = init_config()

init_notifier(app)
init_datadir(app, args)

logging.info("Initializing the video recorder... ")
video_recorder = VideoRecorder(recording_path = app.data_dir)
logging.info("Video recorder initialized successfully.")

if args.no_monitor:
    logging.info("Camera monitor is disabled.")
else:
    logging.info("Starting the camera monitor... ")
    camera_monitor = CameraMonitor(
            video_recorder = video_recorder,
            camera_id = int(app.user_config['CameraID']),
            max_errors = int(app.user_config['MaxErrors']),
            notifier = app.notifier
        )
    camera_monitor.start()
    app.camera_monitor = camera_monitor
    logging.info("Camera monitor started successfully.")

logging.info("Starting the Flask web server... ")
# TODO: Mode port and host to the configuration file and add a command line argument to change it.
if args.debug:
    app.run(host=args.host, port=args.port, debug=True)
else:
    app.run(host=args.host, port=args.port)
