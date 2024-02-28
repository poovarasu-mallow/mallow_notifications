"""Module for sending emails using different mailers.

This module provides a class `EmailMessage` for sending emails using different
mailers, such as SMTP, Amazon SES, and log.
"""


import os
from typing import Optional, Union

from mallow_notifications.base.celery import celery
from mallow_notifications.base.exceptions import MailError
from mallow_notifications.base.logger import get_logger
from mallow_notifications.base.settings import Settings
from mallow_notifications.base.utils import check_required_attributes
from mallow_notifications.mailer.amazon_ses import SESMail
from mallow_notifications.mailer.log import LogMail
from mallow_notifications.mailer.smtp import SMTPMail

settings = Settings()

logging = get_logger(__name__)


def get_mailer(driver, **credentials) -> Union[SMTPMail, SESMail, LogMail]:
    """Create and return a mailer based on the specified driver, using the
    provided credentials.

    :params driver (str): The type of mailer to use, such as "smtp",
        "amazon_ses", "ses", or "log".
    :params credentials (dict): A dictionary containing the credentials
        for the mailer.
    :raises MailError: If the specified driver is not a valid mailer.
    :returns: An instance of the mailer based on the specified driver
        and credentials.
    """
    if driver == "smtp":
        base = SMTPMail
    elif driver in ("amazon_ses", "ses"):
        base = SESMail
    elif driver == "log":
        base = LogMail
    else:
        raise MailError(f"{driver} is not a valid mailer")
    return base(**credentials)


class EmailMessage:
    """Class for sending emails using different mailers."""

    # pylint: disable=too-many-instance-attributes, dangerous-default-value
    def __init__(
        self,
        run_asynk_task: bool = False,
        to: Optional[list] = [],
        from_: Optional[str] = None,
        subject: Optional[str] = None,
        **kwargs,
    ):
        """Initialize the email message with the specified attributes.

        :param run_asynk_task: Whether to run the task asynchronously.
        :param to: A list of email addresses to send the email to.
        :param from_: The sender's email address.
        :param subject: The subject of the email.
        """
        self.run_asynk_task = run_asynk_task
        self.from_ = from_
        self.to = to
        self.cc = kwargs.get("cc", None)
        self.bcc = kwargs.get("bcc", None)
        self.subject = subject
        self.content = {}
        self.attachments = {}

    def set_content(self, content_type: str, content: str) -> None:
        """Sets the content for the specified content type.

        :param content_type: The type of content to set.
        :param content: The content to set.
        :return: None
        """
        self.content[content_type] = content

    def add_attachment(self, file_path: str, filename: Optional[str] = None) -> None:
        """Adds an attachment to the email message.

        :param file_path: The path to the attachment file.
        :param filename: The name of the attachment file.
        :return: None
        """
        if filename is None:
            filename = os.path.basename(file_path)
        self.attachments[filename] = file_path

    @celery.task(bind=True)
    def send_email(self, message_content: dict, driver: str, mailer_credtials: dict) -> None:
        """Send the email using the specified driver and credentials.

        :param message_content: A dictionary containing the email
            message details.
        :param driver: The type of mailer to use, such as "smtp",
            "amazon_ses", "ses", or "log".
        :param mailer_credtials: A dictionary containing the credentials
            for the mailer.
        :return: None
        """
        mailer = get_mailer(driver, **mailer_credtials)
        mailer.send(message_content)

    def send(self):
        """Send the email using the specified driver and credentials."""
        driver = settings.MAIL_DRIVER
        driver_attributes_error_message = "{} is required when driver is configured"
        required_attributes = []
        if driver == "smtp":
            required_attributes = [
                "SMTP_MAIL_BACKEND",
                "SMTP_MAIL_PORT",
                "SMTP_MAIL_USERNAME",
                "SMTP_MAIL_PASSWORD",
                "SMTP_MAIL_USE_SSL",
            ]
            check_required_attributes(required_attributes, driver_attributes_error_message)
            mailer_credtials = {
                "hostname": settings.SMTP_MAIL_BACKEND,
                "port": settings.SMTP_MAIL_PORT,
                "username": settings.SMTP_MAIL_USERNAME,
                "password": settings.SMTP_MAIL_PASSWORD,
                "use_ssl": settings.SMTP_MAIL_USE_SSL,
            }
        elif driver in ("amazon_ses", "ses"):
            required_attributes = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
            check_required_attributes(required_attributes, driver_attributes_error_message)
            mailer_credtials = {
                "aws_access_key_id": settings.AWS_ACCESS_KEY_ID,
                "aws_secret_access_key": settings.AWS_SECRET_ACCESS_KEY,
                "region_name": settings.AWS_REGION,
            }
        else:
            mailer_credtials = {}
        message_content = {
            "from_": self.from_,
            "to": self.to,
            "bcc": self.bcc,
            "cc": self.cc,
            "subject": self.subject,
            "content": self.content,
            "attachments": self.attachments,
        }

        if self.run_asynk_task:
            check_required_error_message = "{} is required when run_asynk_task is set to True"
            celery_required_fields = ["CELERY_RESULT_BACKEND", "CELERY_BROKER_URL"]
            celery_response = check_required_attributes(
                celery_required_fields, check_required_error_message
            )
            if celery_response:
                self.send_email.delay(  # pylint: disable=no-member
                    message_content, driver, mailer_credtials
                )
        else:
            self.send_email(message_content, driver, mailer_credtials)
