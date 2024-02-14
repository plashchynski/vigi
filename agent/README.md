# ViGi — A camera surveillance system

## Requirements

- Python 3.12
- OpenCV
- Camera (webcam or IP camera) that can be accessed via OpenCV
- A server hardware (Raspberry Pi, PC, etc.) to run the agent

## Run from source

```bash
pip3.12 install --upgrade pip
python3.12 -m venv .venv
. .venv/bin/activate

pip3.12 install -r requirements.txt
.venv/bin/flask --debug --app vigi_agent.main run
```
