# Mallow Notification

Mallow Notification is used to send the notication using Amazon SNS and using multiple mail adapters (SMTP, Amazon SES)

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
        <a href="#overview">Overview</a>
    </li>
    <li>
        <a href="#requirements">Requirements</a>
    </li>
     <li>
        <a href="#installation">Installation</a>
        <ul>
            <li><a href="#creating-env">Python-venv</a></li>
            <li><a href="#package-installation">Package Installation</a></li>
        </ul>
        </li>
    <li><a href="#example">Example</a></li>
  </ol>
</details>


## Overview

Project aims to provide a flexible and robust notification system for users, allowing them to efficiently send notifications via Amazon SNS and emails through multiple mail adapters. The architecture is designed to be loosely coupled, ensuring ease of integration within various projects while adhering to SOLID principles to maintain a high level of code quality and extensibility.


## Requirements

* Python 3.10+

## Installation

Assuming that you have a supported version of Python installed, you can first set up your environment with:

#### Creating ENV
* python-venv
  ```sh
  $ python -m venv venv
  ...
  $ venv/bin/activate
  ```
* anaconda env
  ```sh
  $ conda create --name venv python=3.10
  ...
  $ conda activate venv
  ```

#### Package Installation
Install using `pip`
```sh
pip install git+https://github.com/poovarasu-mallow/mallow_notifications.git
```


## Example

Let's take a look at a quick example of using mallow-notification to send notification and emails

Let create an sample file names sample.py

#### Amazon SNS Notification
```
from mallow_notifications.sns.notification_adpater import Notification

notification = Notification()
notification.run_asynk_task = (
    True  # If set to True, it will be sent asynchronously using external celery worker
)
notification.service = PublishMessageProtocol.SMS
notification.phone_number = "+91 1234567890"
notification.subject = faker.pystr(min_chars=1, max_chars=180)
notification.message = faker.pystr(min_chars=1, max_chars=256)
notification.title = faker.pystr(min_chars=1, max_chars=180)
notification.set_data("id", 2) # Optional attributes
notification.set_attributes(
    attribute_key, {"data_key": data_value}
)  # Add optional attributes
notification.send()

```


#### Mailer

```
from mallow_notifications.mailer import EmailMessage

mailer = EmailMessage()
mailer.run_asynk_task = (
    True  # If set to True, it will be sent asynchronously using external celery worker
)
mailer.from_ = (User, user@gmail.com)
mailer.to = [user1@gmail.com, user2@gmail.com]
mailer.subject = "Sample Subject"

# pylint: disable=invalid-name
messgae = "Sample text message"
mailer.set_content("plain", messgae)
mailer.send()

```
