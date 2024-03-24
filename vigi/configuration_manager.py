# this class is used to validate and store the configuration of the agent
import os

import torch

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
        self.detection_model_file = os.path.join(user_data_dir('vigi-agent', 'Vigi'), 'yolov8n.pt')
        self.disable_detection = False
        self.inference_device = 'cpu'
        self.http_basic_username = None
        self.http_basic_password = None
        self.http_basic_hashed_password = None

        # detect if cuda is available
        if torch.cuda.is_available():
            self.set_inference_device('cuda')

        # detect if mps is available (Apple ARM chips)
        elif torch.backends.mps.is_available():
            self.set_inference_device('mps')
        

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

    def set_disable_detection(self, disable_detection):
        # set the disable detection mode
        self.disable_detection = disable_detection

    def set_detection_model_file(self, detection_model_file):
        if not os.path.exists(detection_model_file):
            raise ValueError('Detection model file does not exist')

        self.detection_model_file = detection_model_file

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
        if cmd_args.detection_model_file:
            self.set_detection_model_file(cmd_args.detection_model_file)
        if cmd_args.no_monitor:
            self.no_monitor = True
        if cmd_args.disable_detection:
            self.set_disable_detection(True)
        if cmd_args.inference_device:
            self.set_inference_device(cmd_args.inference_device)
        if cmd_args.http_basic_username:
            self.http_basic_username = cmd_args.http_basic_username
        if cmd_args.http_basic_password:
            self.http_basic_password = cmd_args.http_basic_password

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

    def set_inference_device(self, inference_device):
        # check if device is exist
        try:
            torch.device(inference_device)
        except:
            raise ValueError('Inference device is not valid')

        # set the inference device
        self.inference_device = inference_device

    def update_from_config(self, default_config, camera_configs):
        # update the configuration from the configuration file
        if 'Port' in default_config:
            self.set_port(default_config['Port'])
        if 'Host' in default_config:
            self.set_host(default_config['Host'])
        if 'DataDir' in default_config:
            self.set_data_dir(default_config['DataDir'])
        if 'Debug' in default_config:
            self.set_debug(default_config['Debug'] == 'True')
        if 'NoMonitor' in default_config:
            self.no_monitor = default_config['NoMonitor'] == 'True'
        if 'DetectionModelFile' in default_config:
            self.set_detection_model_file(default_config['DetectionModelFile'])
        if 'DisableDetection' in default_config:
            self.set_disable_detection(default_config['DisableDetection'] == 'True')
        if 'InferenceDevice' in default_config:
            self.set_inference_device(default_config['InferenceDevice'])
        if 'HttpBasicUsername' in default_config:
            self.http_basic_username = default_config['HttpBasicUsername']
        if 'HttpBasicPassword' in default_config:
            self.http_basic_password = default_config['HttpBasicPassword']
        if 'HttpBasicHashedPassword' in default_config:
            self.http_basic_hashed_password = default_config['HttpBasicHashedPassword']

        # SMTP configuration
        if 'smtpServer' in default_config:
            self.smtp_server_config = {}

            smtp_params = ['smtpServer', 'smtpPort', 'smtpUser', 'smtpPassword', 'senderEmail']
            for param in smtp_params:
                self.smtp_server_config[param] = default_config[param]    
            
            self.smtp_server_config['recipientEmails'] = default_config['recipientEmails'].split(',')

        if 'twilioAccountSid' in default_config:
            self.twilio_config = {}

            twilio_params = ['twilioAccountSid', 'twilioAuthToken', 'twilioFromNumber']
            for param in twilio_params:
                self.twilio_config[param] = default_config[param]
            
            self.twilio_config['toNumbers'] = default_config['toNumbers'].split(',')

        for camera_config_info in camera_configs:
            camera_config = CameraConfig()
            camera_config.set_camera_id(camera_config_info['CameraId'])

            if 'MaxErrors' in camera_config_info:
                camera_config.set_max_errors(camera_config_info['MaxErrors'])
            
            if 'Sensitivity' in camera_config_info:
                camera_config.set_sensitivity(camera_config_info['Sensitivity'])

            self.cameras_config[camera_config.camera_id] = camera_config
