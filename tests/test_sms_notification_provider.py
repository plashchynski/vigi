import unittest
from unittest.mock import patch, MagicMock
from vigi.notification_providers.sms_notification_provider import SMSNotificationProvider

class TestSMSNotificationProvider(unittest.TestCase):
    @patch('vigi.notification_providers.sms_notification_provider.Client')
    def test_notify(self, mock_client):
        # Initialize the mocked Twilio client
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance

        provider = SMSNotificationProvider(
            account_sid = "account_sid",
            auth_token = "auth_token",
            from_number = "+11223344",
            recipient_phone_numbers = ["+1234567890", "+9876543210"]
        )


        provider.notify("Test notification")
        mock_client.assert_called_with("account_sid", "auth_token")

        self.assertEqual(mock_client_instance.messages.create.call_count, 2)
