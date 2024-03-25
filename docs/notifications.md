## Notification services

The agent can send notifications using the following channels:
* SMS using Twilio API
* Email using SMTP

### Twilio

To enable SMS notifications, you need to set up a Twilio account and get the following credentials:
* twilio account SID
* twilio auth token

Set this configuration in the `vigi.ini` file.
Consult the [Configuration](docs/configuration.md) document for more details.

### Email

To enable email notifications, you need to set up an SMTP server and get the following credentials:
* SMTP server address
* SMTP server port
* SMTP username
* SMTP password

You can use a Gmail SMTP server for this purpose. Set this configuration in the `vigi.ini` file.
Consult the [Configuration](docs/configuration.md) document for more details.