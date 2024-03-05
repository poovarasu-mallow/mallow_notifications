import smtplib
import unittest
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from unittest import mock
from unittest.mock import MagicMock

from faker import Faker

from mallow_notifications.base.exceptions import MailError, NotificationError
from mallow_notifications.mailer.smtp import SMTPMail


class BaseSMTPMail(unittest.TestCase):
    def setUp(self):
        self.faker = Faker()
        self.mail = SMTPMail(
            hostname=self.faker.pystr(min_chars=1, max_chars=180),
            port=self.faker.random_int(),
            username=self.faker.pystr(min_chars=1, max_chars=180),
            password=self.faker.pystr(min_chars=1, max_chars=180),
            use_ssl=self.faker.pybool(),
        )


class TestSMTPMail(BaseSMTPMail):
    def test_send_success_response(self):
        kwargs = {
            "from_": self.mail._format_emails_address(
                (self.faker.pystr(min_chars=1, max_chars=100), self.faker.email())
            ),
            "to": [self.faker.email()],
            "bcc": [self.faker.email()],
            "cc": [self.faker.email()],
            "subject": self.faker.pystr(min_chars=1, max_chars=180),
            "content": {
                "plain": self.faker.pystr(min_chars=1, max_chars=256),
            },
            "attachments": {},
        }
        with mock.patch("mallow_notifications.mailer.smtp.logging.info") as mock_logging:
            with mock.patch("smtplib.SMTP") as mock_smtp:

                instance = mock_smtp.return_value.__enter__.return_value
                instance.ehlo.return_value = None
                self.mail.send(kwargs)
                instance.ehlo.assert_called_once()
                mock_logging.assert_called_once_with("Email Sent Successfully!")
                instance.send_message.assert_called_once()

    def test_send_success_response_with_attachments(self):
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
        with mock.patch("mallow_notifications.mailer.smtp.logging.info") as mock_logging:
            with mock.patch(
                "builtins.open", mock.mock_open(read_data=b"Fake file content")
            ) as mock_file_open:
                with mock.patch("smtplib.SMTP") as mock_smtp:
                    instance = mock_smtp.return_value.__enter__.return_value
                    instance.ehlo.return_value = None
                    self.mail._add_attachment(
                        temp_file_name,
                        self.faker.binary(length=10),
                        MIMEMultipart("alternative"),
                    )
                    self.mail.send(kwargs)

                    instance.ehlo.assert_called_once()
                    mock_logging.assert_called_once_with("Email Sent Successfully!")
                    instance.send_message.assert_called_once()

    def test_send_without_hostname(self):
        kwargs = {
            "from_": self.faker.email(),
            "to": [self.faker.email()],
            "bcc": [self.faker.email()],
            "cc": [self.faker.email()],
            "subject": self.faker.pystr(min_chars=1, max_chars=180),
            "content": {
                "plain": self.faker.pystr(min_chars=1, max_chars=256),
            },
            "attachments": {},
        }
        self.mail.hostname = None

        with self.assertRaises(MailError):
            self.mail.send(kwargs)

    def test_send_with_ssl_success_response(self):
        kwargs = {
            "from_": self.faker.email(),
            "to": [self.faker.email()],
            "bcc": [self.faker.email()],
            "cc": [self.faker.email()],
            "subject": self.faker.pystr(min_chars=1, max_chars=180),
            "content": {
                "plain": self.faker.pystr(min_chars=1, max_chars=256),
            },
            "attachments": {},
        }

        self.mail.use_ssl = True
        with mock.patch("smtplib.SMTP") as mock_smtp:

            instance = mock_smtp.return_value.__enter__.return_value
            instance.ehlo.return_value = None
            instance.starttls.return_value = None
            self.mail.send(kwargs)
            instance.ehlo.assert_called_once()
            instance.send_message.assert_called_once()

    def test_send_with_ssl_error_response(self):
        kwargs = {
            "from_": self.faker.email(),
            "to": [self.faker.email()],
            "bcc": [self.faker.email()],
            "cc": [self.faker.email()],
            "subject": self.faker.pystr(min_chars=1, max_chars=180),
            "content": {
                "plain": self.faker.pystr(min_chars=1, max_chars=256),
            },
            "attachments": {},
        }

        self.mail.use_ssl = True
        expected_error = smtplib.SMTPNotSupportedError
        with mock.patch("smtplib.SMTP", side_efffect=expected_error) as mock_smtp:

            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            mock_server.starttls.side_effect = smtplib.SMTPNotSupportedError

            with self.assertRaises(MailError) as context:
                self.mail.send(kwargs)

            expected_message = "Server does not suport STARTTLS command"
            self.assertEqual(str(context.exception), expected_message)

            # Ensure that starttls method was called
            mock_server.starttls.assert_called_once()

            # Ensure that other methods were not called
            mock_server.send_message.assert_not_called()
            mock_server.login.assert_not_called()
            mock_server.auth_login.assert_not_called()
