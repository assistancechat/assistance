# Copyright (C) 2023 Assistance.Chat contributors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import base64
import json
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import marko
from mailparser_reply import EmailReplyParser

from assistance import _ctx
from assistance._config import SUPERVISION_SUBJECT_FLAG
from assistance._keys import get_postal_api_key
from assistance._paths import MONOREPO
from assistance._types import Email

POSTAL_API_KEY = get_postal_api_key()

# TODO: Pull this from the config file instead
SIGNATURE = """
Kind regards,

**Alex Carpenter**\\
Head of Development, Solving Australia's Skills Shortage\\
Head of Entrepreneurship

![Alphacrucis University College Logo](cid:logo)

[Linkedin](https://www.linkedin.com/in/alex1carpenter/) | [Twitter](https://twitter.com/Alex1Carpenter)
"""

LOGO_PATH = MONOREPO / "images" / "logo.png"


async def handle_reply_formatter(email: Email):
    subject, body_template = _get_reply_template(email)

    user_email_address = email["agent_name"].split("===")[-1].replace("==", "@")

    mail_from = "Alex Carpenter <pathways@jims.international>"

    message = MIMEMultipart("alternative")
    message["From"] = mail_from
    message["To"] = user_email_address
    message["Subject"] = subject

    plain_body = body_template
    html_body = marko.convert(plain_body)

    plain_text_message = MIMEText(plain_body, "plain", "utf-8")
    html_message = MIMEText(html_body, "html", "utf-8")
    message.attach(plain_text_message)
    message.attach(html_message)

    with open(LOGO_PATH, "rb") as f:
        image = MIMEImage(f.read())

    image.add_header("Content-ID", "logo")
    message.attach(image)

    b64_message = base64.b64encode(message.as_bytes()).decode()

    headers = {
        "Content-Type": "application/json",
        "X-Server-API-Key": POSTAL_API_KEY,
    }

    url = "https://postal.assistance.chat/api/v1/send/raw"

    postal_data = {
        "mail_from": mail_from,
        "rcpt_to": [
            user_email_address,
            "pathways@jims.international",
            "me@simonbiggs.net",
        ],
        "data": b64_message,
    }

    _postal_response = await _ctx.session.post(
        url=url,
        headers=headers,
        data=json.dumps(postal_data),
    )


def _get_reply_template(email: Email):
    parser = EmailReplyParser()
    email_message = parser.read(email["plain_all_content"])

    most_recent_reply = str(email_message.replies[0].body)
    formatting_adjusted_reply = "\n".join(
        [line.lstrip("> ").strip() for line in most_recent_reply.splitlines()]
    )

    formatting_adjusted_reply = formatting_adjusted_reply.replace("\nA:", "  \nA:")

    subject = email["subject"]
    subject = subject.split(SUPERVISION_SUBJECT_FLAG)[-1].strip()

    body_template = formatting_adjusted_reply + "\n\n" + SIGNATURE.strip()

    return subject, body_template
