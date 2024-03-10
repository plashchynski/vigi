# this class is used to validate and store the configuration of the agent
import os

from platformdirs import user_data_dir

class ConfigurationManager:
    def __init__(self):
        # default configuration
        self.port = 5000
        self.host = 'localhost'
        self.data_dir = user_data_dir('vigi-agent', 'Vigi')
        self.camera_id = 0
        self.debug = False
        self.smtp_server_config = None
        self.twilio_config = None
        self.max_errors = 50
        self.no_monitor = False
        self.db_path = os.path.join(self.data_dir, 'vigi.db')
        self.sensitivity = 0.5

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

    def set_camera_id(self, camera_id):
        # validate the camera id
        camera_id = int(camera_id)
        if camera_id < 0:
            raise ValueError('Camera id must be a positive integer')
        self.camera_id = camera_id

    def set_debug(self, debug):
        # set the debug mode
        self.debug = debug

    def set_max_errors(self, max_errors):
        # set the maximum number of consecutive errors when reading a frame from the camera
        max_errors = int(max_errors)
        if max_errors < 0:
            raise ValueError('Max errors must be a positive integer')
        self.max_errors = max_errors

    def set_sensitivity(self, sensitivity):
        # set the sensitivity of the motion detector
        sensitivity = float(sensitivity)
        if sensitivity < 0 or sensitivity > 1:
            raise ValueError('Sensitivity must be between 0 and 1')
        self.sensitivity = sensitivity

    def update_from_args(self, args):
        # update the configuration from the command line arguments
        if args.port:
            self.set_port(args.port)
        if args.host:
            self.set_host(args.host)
        if args.data_dir:
            self.set_data_dir(args.data_dir)
        if args.camera_id:
            self.set_camera_id(args.camera_id)
        if args.debug:
            self.set_debug(True)
        if args.max_errors:
            self.set_max_errors(args.max_errors)
        if args.no_monitor:
            self.no_monitor = True
        if args.sensitivity:
            self.set_sensitivity(args.sensitivity)

    def update_from_config(self, config):
        # update the configuration from the configuration file
        if 'Port' in config:
            self.set_port(config['Port'])
        if 'Host' in config:
            self.set_host(config['Host'])
        if 'DataDir' in config:
            self.set_data_dir(config['DataDir'])
        if 'CameraID' in config:
            self.set_camera_id(config['CameraID'])
        if 'Debug' in config:
            self.set_debug(config['Debug'] == 'True')
        if 'MaxErrors' in config:
            self.set_max_errors(config['MaxErrors'])
        if 'NoMonitor' in config:
            self.no_monitor = config['NoMonitor'] == 'True'
        if 'Sensitivity' in config:
            self.set_sensitivity(config['Sensitivity'])

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
