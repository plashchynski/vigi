# ViGi: A camera surveillance system

## Features

* Motion detection
* Object recognition
* Multiple camera support
* Web server to view the camera feed and recordings
* Notifications via SMS and email

## Requirements

- Python 3.12
- OpenCV
- Camera (webcam or IP camera) that can be accessed via OpenCV
- A server hardware (Raspberry Pi, PC, etc.) to run the agent

## Run from the sources

```bash
# Set up a virtual environment
python3.12 -m venv .venv
. .venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Download a YOLOv8 nano model:
wget https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8n.pt

# run the agent
python main.py
```

## Configuration

The agent can be configured in two ways:
* Using the `vigi.ini` file. This method is recommended for production use and when configuration is
constant and does not change frequently.
* Using command line arguments. This method is recommended for development and testing purposes:

```bash
usage: main.py [-h] [--debug] [--no-monitor] [--data-dir DATA_DIR] [--camera-id CAMERA_ID] [--host HOST] [--port PORT]
               [--max-errors MAX_ERRORS]

options:
  -h, --help            show this help message and exit
  --debug               Enable debug mode
  --no-monitor          Disable the camera monitor
  --data-dir DATA_DIR   Directory to store the recordings
  --camera-id CAMERA_ID
                        Camera ID to monitor
  --host HOST           Host to run the web server
  --port PORT           Port to run the web server
  --max-errors MAX_ERRORS
                        Maximum number of consecutive errors when reading a frame from the camera
```

## Installation on Raspberry Pi (Raspberry Pi OS)

```bash
curl https://pyenv.run | bash # install pyenv

# initialize pyenv:
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

pyenv install 3.12.2 # install Python 3.12
pyenv virtualenv 3.12.2 vigi # create a virtual environment
pyenv activate vigi # activate the virtual environment

# install the required packages
pip install -r requirements.txt

# Download a YOLOv8 nano model:
wget https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8n.pt

# run the agent
python main.py
```

## Debugging Flask app

If you want to run the Flask app in debug mode without the camera monitor, you can do so by running the following command:

```bash
python main.py --debug --no-monitor
```

## Run unit tests

Download a samples dataset for the motion detection tests from [here](https://drive.google.com/file/d/16yQZuHf3xB-Z6zYG6lGxxMP1umbxlIYd/view?usp=sharing) and extract it to the `agent/tests` directory.

Then run the tests:

```bash
python -m unittest discover
```

## Test coverage

To generate a coverage report, run the following command:

```bash
pip install coverage
coverage run -m unittest discover
coverage html
```

# Notification services

The agent can send notifications using the following channels:
* SMS using Twilio API
* Email using SMTP

## Twilio

To enable SMS notifications, you need to set up a Twilio account and get the following credentials:
* twilio account SID
* twilio auth token

Set this configuration in the `vigi.ini` file.

## Email

To enable email notifications, you need to set up an SMTP server and get the following credentials:
* SMTP server address
* SMTP server port
* SMTP username
* SMTP password

You can use a Gmail SMTP server for this purpose. Set this configuration in the `vigi.ini` file.

