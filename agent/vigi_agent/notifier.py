# This file contains the Notifier class which is high level class for sending notifications to different
# notification providers. The providers implement the notify method, such as email, sms, etc.
import logging

class Notifier:
    def __init__(self, providers):
        self.providers = providers

    def notify(self, message):
        logging.info(f"Sending notification: {message}")

        for provider in self.providers:
            provider.notify(message)
