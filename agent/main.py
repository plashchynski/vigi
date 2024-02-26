import configparser

from vigi_agent.app import app
from vigi_agent.camera_monitor import CameraMonitor

# Read the configuration file
print("Reading the configuration file... ", end="", flush=True)
config = configparser.ConfigParser()
config.read('vigi.ini')
app.user_config = config['DEFAULT']
print("done!", flush=True)

camera_monitor = CameraMonitor(camera_id=int(app.user_config['CameraID']))
camera_monitor.start()
app.camera_monitor = camera_monitor

# run Flask app
app.run(host='127.0.0.1', port=5000)
