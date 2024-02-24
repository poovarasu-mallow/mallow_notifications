import unittest
from email.mime.text import MIMEText
from unittest import mock
from unittest.mock import MagicMock

from faker import Faker

from mallow_notifications.mailer.log import LogMail


class BaseLogMail(unittest.TestCase):
    def setUp(self):
        self.mail = LogMail()
        self.faker = Faker()


class TestLogMail(BaseLogMail):
    def test_send_success_response(self):
        kwargs = {
            "from_": self.faker.email(),
            "to": [self.faker.email()],
            "bcc": [self.faker.email()],
            "cc": [self.faker.email()],
            "subject": self.faker.pystr(min_chars=1, max_chars=180),
            "content": {
                "plain": self.faker.pystr(min_chars=1, max_chars=256),
            },
        }
        with mock.patch("mallow_notifications.mailer.log.logging.info") as mock_logging_info:
            self.mail.send(kwargs)
            mock_logging_info.assert_called_once_with(mock.ANY)
