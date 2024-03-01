import argparse
import logging
import configparser

from vigi_agent.notification_providers.email_notification_provider import EmailNotificationProvider
from vigi_agent.notification_providers.sms_notification_provider import SMSNotificationProvider
from vigi_agent.notifier import Notifier

parser = argparse.ArgumentParser()
# TODO: Add a help argument to show the help message.
parser.add_argument("--debug", help="Enable debug mode", action='store_true')
parser.add_argument("--no-monitor", help="Disable the camera monitor", action='store_true')
args = parser.parse_args()

if args.debug:
    logging.basicConfig(level=logging.DEBUG)
else:
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

notifier = Notifier(notification_providers)
logging.info("Notifier initialized successfully.")

logging.info("Initializing the video recorder... ")
video_recorder = VideoRecorder(recording_path = app.user_config['RecordingsPath'])
logging.info("Video recorder initialized successfully.")

if args.no_monitor:
    logging.info("Camera monitor is disabled.")
else:
    logging.info("Starting the camera monitor... ")
    camera_monitor = CameraMonitor(
            video_recorder = video_recorder,
            camera_id = int(app.user_config['CameraID']),
            max_errors = int(app.user_config['MaxErrors']),
            notifier = notifier
        )
    camera_monitor.start()
    app.camera_monitor = camera_monitor
    logging.info("Camera monitor started successfully.")

logging.info("Starting the Flask web server... ")
# TODO: Mode port and host to the configuration file and add a command line argument to change it.
if args.debug:
    app.run(host='127.0.0.1', port=5000, debug=True)
else:
    app.run(host='127.0.0.1', port=5000)

