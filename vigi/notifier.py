"""
This file contains the Notifier class which is high level class for
sending notifications to different notification providers.
The providers implement the notify method, such as email, sms, etc.
"""

import logging

class Notifier:
    """
    The Notifier class is a high level class for sending notifications to
    different notification providers.
    """
    def __init__(self, providers):
        self.providers = providers

    def notify(self, message):
        """
        Send a notification to all the providers.
        """
        logging.info("Sending notification: %s", message)

        for provider in self.providers:
            provider.notify(message)
