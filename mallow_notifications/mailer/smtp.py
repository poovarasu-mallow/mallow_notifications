"""Module for sending emails using SMTP.

This module provides a class `SMTPMail` for sending emails using SMTP.
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from typing import Optional

from mallow_notifications.base.exceptions import MailError
from mallow_notifications.base.logger import get_logger
from mallow_notifications.mailer.base import BaseMail

logging = get_logger(__name__)


class SMTPMail(BaseMail):
    """Class for sending emails using SMTP.

    This class provides a method to send an email message using the SMTP
    protocol.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        hostname: Optional[str] = None,
        port: Optional[int] = 25,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_ssl: Optional[bool] = True,
    ):
        """Initialize the SMTP credentials with the provided hostname, port,
        username, password, and use_ssl.

        :param hostname: Optional[str] - The SMTP hostname
        :param port: Optional[int] - The SMTP port
        :param username: Optional[str] - The SMTP username
        :param password: Optional[str] - The SMTP password
        :param use_ssl: Optional[bool] - Whether to use SSL
        """
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.use_ssl = use_ssl

    def send(self, message: dict) -> None:
        """A function to send an email message using the SMTP protocol.

        :param message: A dictionary containing the email message
            details.
        :type message: dict
        :return: None
        """
        if self.hostname is None:
            raise MailError("Hostname is not set")

        email = MIMEMultipart("alternative")
        email["From"] = self._format_emails_address(message["from_"])
        email["To"] = ",".join(message["to"])
        email["Subject"] = message["subject"]

        self._compose_extra_emails(message, email)

        for type_, content in message["content"].items():
            self._build_multipart_content(email, type_, content)

        for filename, file in message["attachments"].items():
            self._add_attachment(file, filename, email)

        # pylint: disable=raise-missing-from
        with smtplib.SMTP(self.hostname, self.port) as server:
            if self.username is not None:
                server.user = self.username
                server.password = self.password
            try:
                server.ehlo()
                if self.use_ssl:
                    try:
                        server.starttls()
                    except smtplib.SMTPNotSupportedError:
                        raise MailError("Server does not suport STARTTLS command")
                if self.username:
                    server.auth_login()
                    server.login(self.username, self.password)

                server.send_message(email)
                logging.info("Email Sent Successfully!")
            except (
                smtplib.SMTPConnectError,
                smtplib.SMTPSenderRefused,
                smtplib.SMTPAuthenticationError,
                smtplib.SMTPRecipientsRefused,
                smtplib.SMTPServerDisconnected,
                smtplib.SMTPException,
            ) as e:
                raise MailError(f"SMTP Error: {str(e)}")
