"""Module for logging mail sending operations.

This module provides a class `LogMail` for logging details of mail sending operations.
The `LogMail` class inherits from `BaseMail` and overrides its `send` method to include
logging functionality.
"""

from email.mime.text import MIMEText

from mallow_notifications.base.logger import get_logger
from mallow_notifications.mailer.base import BaseMail

logging = get_logger(__name__)


class LogMail(BaseMail):
    """Class for logging mail sending.

    This class provides a method to log the details of a mail send
    operation.
    """

    def send(self, message: dict) -> None:
        """Sends the mail and logs the details of the operation."""
        mail_content = None
        content_type = None
        for type_, content in message["content"].items():
            mail_content = content
            content_type = type_

        content = MIMEText(mail_content, content_type)

        logging.info(  # pylint: disable=logging-fstring-interpolation
            f'Mail Send Successfully\nFrom: {self._format_emails_address(message["from_"])}\nTo: {",".join(message["to"])}\n{"Bcc"}: {",".join(message["bcc"]) if message["bcc"] else ""}\n{"Cc"}: {",".join(message["cc"]) if message["cc"] else ""}\nSubject: {message["subject"]}\nContent: {content}'  # pylint: disable=line-too-long
        )
