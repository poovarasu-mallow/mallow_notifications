"""This module contains the `SESMail` class for sending emails using Amazon
SES."""

from email.mime.multipart import MIMEMultipart
from typing import Optional

import boto3

from mallow_notifications.base.constants import AmazonSerives
from mallow_notifications.base.exceptions import MailError
from mallow_notifications.base.logger import get_logger
from mallow_notifications.mailer.base import BaseMail

logging = get_logger(__name__)


class SESMail(BaseMail):
    """Class for sending emails using Amazon SES."""

    def __init__(
        self,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        region_name: Optional[str] = None,
    ):
        """Initialize the AWS credentials with the provided access key, secret
        key, and region.

        :param aws_access_key_id: Optional[str] - The AWS access key ID
        :param aws_secret_access_key: Optional[str] - The AWS secret access key
        :param region_name: Optional[str] - The AWS region name
        """
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.client = boto3.client(
            AmazonSerives.SES,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region_name,
        )

    def _check_sending_enabled(self) -> None:
        """Check if email sending is enabled for the account."""
        account_sending_info = self.client.get_account_sending_enabled()
        if "Enabled" in account_sending_info and not account_sending_info["Enabled"]:
            raise MailError("Email sending has been disabled in your region.")

    def _check_quota(self) -> None:
        """Check the quota for sending emails and raise a MailError if the
        maximum 24-hour send limit has been reached."""
        send_quota = self.client.get_send_quota()
        if send_quota["SentLast24Hours"] == send_quota["Max24HourSend"]:
            raise MailError(
                f"Maximum mail sending reached for last 24 hours. You have sent {send_quota['SentLast24Hours']} emails out of {send_quota['Max24HourSend']} in the last 24 hours."  # pylint: disable=line-too-long
            )

    def send(self, message: dict) -> None:
        """A function to send an email message using the Amazon SES protocol.

        :param message: A dictionary containing the email message
            details.
        :type message: dict
        :return: None
        """
        email = MIMEMultipart("alternative")
        email["From"] = self._format_emails_address(message["from_"])
        email["To"] = ",".join(message["to"])
        email["Subject"] = message["subject"]

        for type_, content in message["content"].items():
            self._build_multipart_content(email, type_, content)

        for filename, file in message["attachments"].items():
            self._add_attachment(file, filename, email)

        self._compose_extra_emails(message, email)

        try:
            self._check_sending_enabled()
            self._check_quota()
            raw_message = email.as_string()
            self.client.send_raw_email(RawMessage={"Data": raw_message})
            logging.info("Email Sent Successfully!")
        except (
            self.client.exceptions.MessageRejected,
            self.client.exceptions.MailFromDomainNotVerifiedException,
            self.client.exceptions.ConfigurationSetDoesNotExistException,
            self.client.exceptions.ConfigurationSetSendingPausedException,
            self.client.exceptions.AccountSendingPausedException,
        ) as e:
            raise MailError(f"Amazon SES Error: {str(e)}")  # pylint: disable=raise-missing-from
