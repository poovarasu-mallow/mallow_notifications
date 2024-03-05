"""This example shows how to send notifications using the `Notification`
class."""

from faker import Faker

from mallow_notifications.base.constants import PublishMessageProtocol
from mallow_notifications.sns.notification_adpater import Notification

faker = Faker()

attribute_key = faker.pystr(min_chars=1, max_chars=50)
attribute_value = faker.pystr(min_chars=1, max_chars=100)

notification = Notification()
notification.run_asynk_task = (
    True  # If set to True, it will be sent asynchronously using external celery worker
)
notification.service = PublishMessageProtocol.SMS
notification.phone_number = "+91 1234567890"
notification.subject = faker.pystr(min_chars=1, max_chars=180)
notification.message = faker.pystr(min_chars=1, max_chars=256)
notification.title = faker.pystr(min_chars=1, max_chars=180)
notification.set_attributes(
    attribute_key, {"data_type": attribute_value}
)  # Add optional attributes
notification.send()
