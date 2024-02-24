"""This example shows how to send emails using the `EmailMessage` class."""

from faker import Faker

from mallow_notifications.mailer import EmailMessage

faker = Faker()
mx = EmailMessage()
mx.run_asynk_task = (
    True  # If set to True, it will be sent asynchronously using external celery worker
)
mx.from_ = (faker.name(), faker.email())
mx.to = [faker.email()]
mx.subject = faker.pystr(min_chars=1, max_chars=180)

# pylint: disable=invalid-name
messgae = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Sample Heading </h1>
    <p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. Doloribus at quam ipsa animi reiciendis repudiandae facere exercitationem iusto. Amet debitis consequatur quia veniam inventore eius sint repudiandae perferendis blanditiis accusamus?</p>
</body>
</html>"""
mx.set_content("html", messgae)
mx.send()
