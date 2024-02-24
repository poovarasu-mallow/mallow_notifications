import smtplib
import unittest
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from unittest import mock
from unittest.mock import MagicMock

from faker import Faker

from mallow_notifications.base.exceptions import MailError
from mallow_notifications.mailer.amazon_ses import SESMail


class BaseSESMail(unittest.TestCase):
    def setUp(self):
        self.faker = Faker()
        self.mail = SESMail(
            aws_access_key_id=self.faker.pystr(min_chars=1, max_chars=180),
            aws_secret_access_key=self.faker.pystr(min_chars=1, max_chars=180),
            region_name=self.faker.pystr(min_chars=1, max_chars=180),
        )


class TestSESMail(BaseSESMail):
    def test_send_success_response(self):
        kwargs = {
            "from_": self.mail._format_emails_address(
                (self.faker.pystr(min_chars=1, max_chars=100), self.faker.email())
            ),
            "to": [self.faker.email()],
            "to": [self.faker.email()],
            "bcc": [self.faker.email()],
            "cc": [self.faker.email()],
            "subject": self.faker.pystr(min_chars=1, max_chars=180),
            "content": {
                "plain": self.faker.pystr(min_chars=1, max_chars=256),
            },
            "attachments": {},
        }

        with mock.patch("mallow_notifications.mailer.amazon_ses.logging.info") as mock_logging:
            with mock.patch(
                "mallow_notifications.mailer.amazon_ses.SESMail._check_sending_enabled"
            ) as mock_sending_enabled:
                with mock.patch(
                    "mallow_notifications.mailer.amazon_ses.SESMail._check_quota"
                ) as mock_quota:

                    with mock.patch("boto3.client") as mock_client:
                        mock_client.client = MagicMock()
                        mock_get_send_quota_response = MagicMock(
                            return_value={"SentLast24Hours": 50, "Max24HourSend": 100}
                        )
                        mock_sending_enabled_response = MagicMock(return_value={"Enabled": True})

                        mock_client.client.get_account_sending_enabled = (
                            mock_sending_enabled_response
                        )
                        mock_sending_enabled.return_value = mock.MagicMock()

                        mock_client.client.get_send_quota = mock_get_send_quota_response
                        mock_quota.return_value = mock.MagicMock()

                        mock_send_raw_email = mock_client.return_value.send_raw_email
                        mock_send_raw_email.return_value = "Success"
                        self.mail.send(kwargs)
                        mock_logging.assert_called_once_with("Email Sent Successfully!")

    def test_send_success_response_with_attachment(self):
        temp_file_name = f"{self.faker.name()}.txt"
        kwargs = {
            "from_": self.faker.email(),
            "to": [self.faker.email()],
            "bcc": [self.faker.email()],
            "cc": [self.faker.email()],
            "subject": self.faker.pystr(min_chars=1, max_chars=180),
            "content": {
                "plain": self.faker.pystr(min_chars=1, max_chars=256),
            },
            "attachments": {temp_file_name: self.faker.binary(length=10)},
        }

        with mock.patch("mallow_notifications.mailer.amazon_ses.logging.info") as mock_logging:
            with mock.patch(
                "builtins.open", mock.mock_open(read_data=b"Fake file content")
            ) as mock_file_open:
                with mock.patch(
                    "mallow_notifications.mailer.amazon_ses.SESMail._check_sending_enabled"
                ) as mock_sending_enabled:
                    with mock.patch(
                        "mallow_notifications.mailer.amazon_ses.SESMail._check_quota"
                    ) as mock_quota:

                        with mock.patch("boto3.client") as mock_client:
                            mock_client.client = MagicMock()
                            mock_get_send_quota_response = MagicMock(
                                return_value={
                                    "SentLast24Hours": 50,
                                    "Max24HourSend": 100,
                                }
                            )
                            mock_sending_enabled_response = MagicMock(
                                return_value={"Enabled": True}
                            )

                            mock_client.client.get_account_sending_enabled = (
                                mock_sending_enabled_response
                            )
                            mock_sending_enabled.return_value = mock.MagicMock()

                            mock_client.client.get_send_quota = mock_get_send_quota_response
                            mock_quota.return_value = mock.MagicMock()
                            self.mail._add_attachment(
                                temp_file_name,
                                self.faker.binary(length=10),
                                MIMEMultipart("alternative"),
                            )
                            mock_send_raw_email = mock_client.return_value.send_raw_email
                            mock_send_raw_email.return_value = "Success"
                            self.mail.send(kwargs)
                            mock_logging.assert_called_once_with("Email Sent Successfully!")

    def test_check_sending_enabled(self):
        with mock.patch("boto3.client") as mock_client:
            mock_client.client = MagicMock()

            mock_client.client.get_account_sending_enabled.return_value = {"Enabled": False}
