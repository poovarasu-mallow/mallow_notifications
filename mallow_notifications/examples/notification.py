"""This example shows how to send notifications using the `Notification`
class."""

from faker import Faker

from mallow_notifications.base.constants import PUBLISH_MESSAGE_PROTOCOLS
from mallow_notifications.sns.notification_adpater import Notification

faker = Faker()

attribute_key = faker.pystr(min_chars=1, max_chars=50)
attribute_value = faker.pystr(min_chars=1, max_chars=100)

notification = Notification()
notification.run_asynk_task = (
    True  # If set to True, it will be sent asynchronously using external celery worker
)
notification.service = PUBLISH_MESSAGE_PROTOCOLS["EMAIL"]
notification.topic_arn = "arn:aws:sns:us-east-1:111111111111:test"  # Sample topic ARN
notification.subject = faker.pystr(min_chars=1, max_chars=180)
notification.message = faker.pystr(min_chars=1, max_chars=256)
notification.title = faker.pystr(min_chars=1, max_chars=180)
notification.set_data("id", 2)
notification.set_attributes(
    attribute_key, {"data_type": attribute_value}
)  # Add optional attributes
notification.send()
