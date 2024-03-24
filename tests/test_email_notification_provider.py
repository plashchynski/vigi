"""
This module contains the tests for the EmailNotificationProvider class.
"""

import unittest
from unittest.mock import patch

from vigi.notification_providers.email_notification_provider import EmailNotificationProvider

# # to have a wild test, please provide your own email credentials
# # and uncomment the following lines:
# class TestEmailNotificationProviderWild(unittest.TestCase):
#     def test_notify(self):
#         # notify should send an email to each recipient
#         provider = EmailNotificationProvider(
#             smtp_server = "smtp.gmail.com",
#             smtp_port = 587,
#             smtp_user = "...",
#             smtp_password = "...",
#             sender_email = "...",
#             recipient_emails = ["..."]
#         )
#         provider.notify("Test notification")

class TestEmailNotificationProvider(unittest.TestCase):
    """
    Test the EmailNotificationProvider class
    """
    @patch('vigi.notification_providers.email_notification_provider.smtplib.SMTP')
    def test_notify(self, mock_smtp):
        """
        Test that the notify method sends an email to each recipient
        """
        provider = EmailNotificationProvider(
            smtp_server = "smtp.gmail.com",
            smtp_port = 587,
            smtp_user = "user",
            smtp_password = "password",
            sender_email = "sender@example.com",
            recipient_emails = ["recipient1@example.com",
                                "recipient2@example.com"]
        )
        provider.notify("Test notification")

        # Verify SMTP was called twice (once for each recipient)
        self.assertEqual(mock_smtp.call_count, 2)
