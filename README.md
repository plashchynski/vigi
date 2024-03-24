# ViGi: A camera surveillance system

## Features

* Multiple camera support
* Motion detection
* Object recognition
* Web server to view the camera feed and recordings
* Notifications via SMS and email

## Requirements

- Python 3.8 or higher. Tested with Python 3.12
- OpenCV
- A USB camera that can be accessed via OpenCV

## Installation and usage

```bash
pip install vigi
vigi
```

## Configuration

A detailed configuration options are available in the [Configuration](docs/configuration.md) document.

The agent can be configured in two ways:
* Using the `vigi.ini` file. This method is recommended for production use and when configuration is
constant and does not change frequently.
* Using command line arguments. This method is recommended for development and testing purposes:

```txt
usage: vigi [-h] [--debug] [--no-monitor] [--data-dir DATA_DIR] [--camera-id CAMERA_ID] [--host HOST] [--port PORT] [--max-errors MAX_ERRORS]
               [--sensitivity SENSITIVITY] [--detection-model-file DETECTION_MODEL_FILE] [--disable-detection]

optional arguments:
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
  --sensitivity SENSITIVITY
                        Sensitivity of the motion detector, should be a float between 0 and 1
  --detection-model-file DETECTION_MODEL_FILE
                        Path to the detection model file (YOLO's yolov8n.pt, by default)
  --disable-detection   Disable object detection
```

You can configure additional cameras by adding a [CAMERAn] section to the `vigi.ini` file, where n is the camera ID. The only required parameter is the `CameraID`:

```ini
[CAMERA0]
CameraID = 0

[CAMERA1]
CameraID = 1

MaxErrors=50
Sensitivity=0.5

```

You can specify `MaxErrors` and `Sensitivity` for each camera separately. If these parameters are not specified, the default values will be used.


## Installation on Raspberry Pi (Raspberry Pi OS)

64 bit OS is required for PyTorch to work. Tested with [Raspberry Pi OS (Legacy, 64-bit)](https://www.raspberrypi.com/software/operating-systems/#raspberry-pi-os-legacy-64-bit).

Install the pip package:
```bash
pip install vigi
```

Run the agent:
```bash
./.local/bin/vigi --host 0.0.0.0
```

# Development

## Run from the sources

```bash
# Set up a virtual environment
python -m venv .venv
. .venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Download a YOLOv8 nano model:
wget https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8n.pt

# run the agent
python main.py
```

## Build a pip package

```bash
pip install build
python -m build
```

## Publish the package to PyPI

```bash
python -m pip install --upgrade twine
python -m twine upload dist/*
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
