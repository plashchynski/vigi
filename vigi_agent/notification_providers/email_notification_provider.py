# This file contains the EmailNotificationProvider class which is used to send email notifications
import logging

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailNotificationProvider:
    def __init__(self, smtp_server: str, smtp_port: int, smtp_user: str, smtp_password: str, sender_email: str,
                 recipient_emails: list):
        """
        :param smtp_server: SMTP server address
        :param smtp_port: SMTP server port
        :param smtp_user: SMTP server user
        :param smtp_password: SMTP server password
        :param sender_email: Email address of the sender
        :param recipient_emails: List of email addresses of the recipients
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.sender_email = sender_email
        self.recipient_emails = recipient_emails
        logging.info(f"EmailNotificationProvider initialized with sender_email: {sender_email}, recipient_emails: {recipient_emails}")

    def notify(self, notification_text: str):
        """
        Send email notification to the recipients
        """
        for recipient_email in self.recipient_emails:
            self._send_email(notification_text, recipient_email)

    def _send_email(self, notification_text: str, recipient_email: str):
        """
        Send email to a single recipient
        """
        logging.info(f"Sending email from {self.sender_email} to {recipient_email} with text: {notification_text}")

        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = recipient_email
        message["Subject"] = "ViGi Agent Notification"
        message.attach(MIMEText(notification_text, 'plain'))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.sender_email, recipient_email, message.as_string())
