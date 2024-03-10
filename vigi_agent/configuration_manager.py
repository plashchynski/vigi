# this class is used to validate and store the configuration of the agent
import os

from platformdirs import user_data_dir

from .camera_config import CameraConfig

class ConfigurationManager:
    def __init__(self):
        # default configuration
        self.port = 5000
        self.host = 'localhost'
        self.data_dir = user_data_dir('vigi-agent', 'Vigi')
        self.debug = False
        self.smtp_server_config = None
        self.twilio_config = None
        self.no_monitor = False
        self.db_path = os.path.join(self.data_dir, 'vigi.db')
        self.cameras_config = {}

    def set_port(self, port):
        # validate the port
        port = int(port)
        if port < 0 or port > 65535:
            raise ValueError('Port must be between 0 and 65535')
        self.port = port
    
    def set_host(self, host):
        # validate the host
        if host == '':
            raise ValueError('Host must not be empty')
        self.host = host

    def set_data_dir(self, data_dir):
        # validate the data directory
        if data_dir == '':
            raise ValueError('Data directory must not be empty')
        self.data_dir = data_dir
        self.db_path = os.path.join(self.data_dir, 'vigi.db')

    def set_debug(self, debug):
        # set the debug mode
        self.debug = debug

    def update_from_args(self, cmd_args):        
        # update the configuration from the command line arguments
        if cmd_args.port:
            self.set_port(cmd_args.port)
        if cmd_args.host:
            self.set_host(cmd_args.host)
        if cmd_args.data_dir:
            self.set_data_dir(cmd_args.data_dir)
        if cmd_args.debug:
            self.set_debug(True)
        if cmd_args.no_monitor:
            self.no_monitor = True

        # configure at leas one camera
        camera_id = 0
        if cmd_args.camera_id is not None:
            camera_id = cmd_args.camera_id

        # configure the camera
        camera_config = CameraConfig()
        camera_config.set_camera_id(camera_id)

        if cmd_args.max_errors:
            camera_config.set_max_errors(cmd_args.max_errors)
        if cmd_args.sensitivity:
            cmd_args.set_sensitivity(cmd_args.sensitivity)

        self.cameras_config[camera_id] = camera_config

    def update_from_config(self, config):
        # update the configuration from the configuration file
        if 'Port' in config:
            self.set_port(config['Port'])
        if 'Host' in config:
            self.set_host(config['Host'])
        if 'DataDir' in config:
            self.set_data_dir(config['DataDir'])
        # if 'CameraID' in config:
        #     self.set_camera_id(config['CameraID'])
        if 'Debug' in config:
            self.set_debug(config['Debug'] == 'True')
        # if 'MaxErrors' in config:
        #     self.set_max_errors(config['MaxErrors'])
        if 'NoMonitor' in config:
            self.no_monitor = config['NoMonitor'] == 'True'
        # if 'Sensitivity' in config:
        #     self.set_sensitivity(config['Sensitivity'])

        # SMTP configuration
        if 'smtpServer' in config:
            self.smtp_server_config = {}

            smtp_params = ['smtpServer', 'smtpPort', 'smtpUser', 'smtpPassword', 'senderEmail']
            for param in smtp_params:
                self.smtp_server_config[param] = config[param]    
            
            self.smtp_server_config['recipientEmails'] = config['recipientEmails'].split(',')

        if 'twilioAccountSid' in config:
            self.twilio_config = {}

            twilio_params = ['twilioAccountSid', 'twilioAuthToken', 'twilioFromNumber']
            for param in twilio_params:
                self.twilio_config[param] = config[param]
            
            self.twilio_config['toNumbers'] = config['toNumbers'].split(',')
