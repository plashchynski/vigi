# ViGi: A camera surveillance system

## Requirements

- Python 3.12
- OpenCV
- Camera (webcam or IP camera) that can be accessed via OpenCV
- A server hardware (Raspberry Pi, PC, etc.) to run the agent

## Run from the sources

```bash
# Set up a virtual environment
cd agent
python3.12 -m venv .venv
. .venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Download a YOLOv8 nano model:
wget https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8n.pt

# run the agent
python main.py
```

## Run unit tests

Download a samples dataset for the motion detection tests from [here](https://drive.google.com/file/d/16yQZuHf3xB-Z6zYG6lGxxMP1umbxlIYd/view?usp=sharing) and extract it to the `agent/tests` directory.

Then run the tests:

```bash
cd agent
python -m unittest tests/*.py
```
