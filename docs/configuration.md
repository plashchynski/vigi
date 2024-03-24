# Configuration

There are two ways to configure the application:
* Using command line arguments
* Using a configuration file

The command line arguments take precedence over the configuration file.

## Command line arguments

The following command line arguments are available:

`--debug` - Enable debug mode, which will print additional information to the console and add debug annotations to the generated video recordings

`--no-monitor` - It is possible to run the agent without the camera monitors. In this case, the agent will serve as a web console.

`--data-dir` - The directory where the agent will store the generated video recordings and other working files. The default value is a system-specified directory for temporary files.

`--camera-id` — The integer ID of the camera to use. The default value is 0. If you have multiple cameras set up, it is possible to specify several camera profiles in the configuration file. Command line arguments will override the first camera profile.

`--host` - The address to bind the web server to. The default value is `localhost`. Make sure to set it to the public IP if you want to access the web console from another device.

`--port` - The port to bind the web server to. The default value is `5000`.

`--max-errors` - The maximum number of camera read errors before the agent stops. The default value is `50`.

`--sensitivity` - Specify sensitivity for motion detection (0.0-1.0). The default value is `0.5`.

`--detection-model-file` — Path to an object detection deep learning model file. By default, the system will download the model from the internet during the first run and store it into `--data-dir`.

`--disable-detection` — Disable object detection. Use it if detection is too slow for you hardware.

`--inference-device` — "cuda" or "cpu". By default it detects automatically if GPU is available. If not, it uses CPU.

`--http-basic-username` — Username for HTTP Basic Authentication for the web console.

`--http-basic-password` — Password for HTTP Basic Authentication for the web console.

`--http-basic-hashed-password` — Hashed password for HTTP Basic Authentication for the web console. This is a more secure way to store the password in the configuration file. Use `scripts/generate_password.py` to generate the hashed password.

## Configuration file

The configuration file is an INI file with the following sections:

`[DEFAULT]` - General settings for all cameras

`Port` - The port to bind the web server to. The default value is `5000`.

`Host` - The address to bind the web server to. The default value is `localhost`. Make sure to set it to the public IP if you want to access the web console from another device.

`DataDir` - The directory where the agent will store the generated video recordings and other working files. The default value is a system-specified directory for temporary files.

`Debug` - Enable debug mode, which will print additional information to the console and add debug annotations to the generated video recordings

`NoMonitor` - It is possible to run the agent without the camera monitors. In this case, the agent will serve as a web console.

`DetectionModelFile` - Path to an object detection deep learning model file. By default, the system will download the model from the internet during the first run and store it into `DataDir`.

`DisableDetection` - Disable object detection. Use it if detection is too slow for you hardware.

`InferenceDevice` - "cuda" or "cpu". By default it detects automatically if GPU is available. If not, it uses CPU.

HTTP Basic Authentication for the web console:

`HttpBasicUsername` - Username for HTTP Basic Authentication for the web console.

`HttpBasicPassword` - Password for HTTP Basic Authentication for the web console.

`HttpBasicHashedPassword` - Hashed password for HTTP Basic Authentication for the web console. This is a more secure way to store the password in the configuration file. Use `scripts/generate_password.py` to generate the hashed password.

The following settings are for Email notifications:

`smtpServer` - SMTP server address for sending email notifications

`smtpPort` - SMTP server port for sending email notifications

`smtpUser` - SMTP server username for sending email notifications

`smtpPassword` - SMTP server password for sending email notifications

`senderEmail` - Email address to send notifications from

`recipientEmails` - Comma-separated list of email addresses to send notifications to

The following settings are for SMS notifications:

`twilioAccountSid` - Twilio account SID for sending SMS notifications

`twilioAuthToken` - Twilio auth token for sending SMS notifications

`twilioFromNumber` - Twilio phone number to send SMS notifications from

`toNumbers` - Comma-separated list of phone numbers to send SMS notifications to

`[Camera0]` - Settings for the first camera. Could be any number of camera sections. The section name should be `Camera` followed by the camera ID: `[Camera0]`, `[Camera1]`, etc.

`CameraId` - The integer ID of the camera to use.

`MaxErrors` - The maximum number of camera read errors before the agent stops. The default value is `50`.

`Sensitivity` - Specify sensitivity for motion detection (0.0-1.0). The default value is `0.5`.
