"""This module contains the `BaseMail` class for sending emails."""

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional, Union


class BaseMail:
    """Mail Base class contains the helper functions for sending emails."""

    def _format_emails_address(self, email_address: Union[str, tuple]):
        """Format the email address by adding the name if provided, and return
        the formatted email address.

        :param email_address: The email address to be formatted
        :type email_address: Union[str, tuple]
        :return: The formatted email address
        :rtype: str
        """
        name = None
        if isinstance(email_address, tuple):
            name, email_address = email_address

        if name is not None:
            parsed = f"{name} <{email_address}>"
            return parsed
        return f"<{email_address}>"

    def _build_multipart_content(self, email: MIMEMultipart, type_: str, content: str):
        """Build multipart content and attach it to the email.

        :param email: The email to attach the content to
        :type email: MIMEMultipart
        :param type_: The type of content
        :type type_: str
        :param content: The actual content to attach
        :type content: str
        :return: None
        """
        data = MIMEText(content, type_)
        email.attach(data)

    def _add_attachment(self, file_path: str, filename: Optional[str], msg: MIMEMultipart) -> None:
        """Add an attachment to the email message.

        :param file_path: The path to the file
        :type file_path: str
        :param filename: The filename
        :type filename: Optional[str]
        :param msg: The email message
        :type msg: MIMEMultipart
        :return: None
        """
        with open(file_path, "rb") as attachment_file:
            part = MIMEApplication(attachment_file.read())
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={file_path if not filename else filename}",
            )
            msg.attach(part)

    def _compose_extra_emails(
        self,
        messgae: dict,
        msg: MIMEMultipart,
    ) -> None:
        """Add extra emails to the email message.

        :param messgae: The email message
        :type messgae: dict
        :param msg: The email message
        :type msg: MIMEMultipart
        :return: None
        """
        if "cc" in messgae and messgae["cc"] is not None:
            msg["Cc"] = ",".join(messgae["cc"])
        if "bcc" in messgae and messgae["bcc"] is not None:
            msg["Bcc"] = ",".join(messgae["bcc"])
