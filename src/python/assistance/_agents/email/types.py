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

from typing import Literal, TypedDict

# Spam and Unknown are guessed here
SpamStatus = Literal["NotSpam", "Spam", "Unknown"]

RawEmail = TypedDict(
    "RawEmail",
    {
        "attachment_quantity": int,
        "attachments": list,
        "auto_submitted": None,
        "bounce": bool,
        "cc": str | None,
        "date": str,
        "from": str,
        "html_body": str,
        "id": int,
        "in_reply_to": str | None,
        "mail_from": str,
        "message_id": str,
        "plain_body": str,
        "rcpt_to": str,
        "received_with_ssl": bool,
        "references": None,
        "replies_from_plain_body": None | str,
        "reply_to": None | str,
        "size": str,
        "spam_status": SpamStatus,
        "subject": str,
        "timestamp": float,
        "to": str,
        "token": str,
    },
)


Email = TypedDict(
    "Email",
    {
        "attachment_quantity": int,
        "attachments": list,
        "auto_submitted": None,
        "bounce": bool,
        "cc": str,
        "date": str,
        "from": str,
        "html_body": str,
        "id": int,
        "in_reply_to": str,
        "mail_from": str,
        "message_id": str,
        "plain_all_content": str,
        "plain_no_replies": str,
        "rcpt_to": str,
        "received_with_ssl": bool,
        "references": None,
        "plain_replies_only": str,
        "reply_to": str,
        "size": str,
        "spam_status": SpamStatus,
        "subject": str,
        "timestamp": float,
        "to": str,
        "token": str,
        "agent_name": str,
        "user_email": str,
    },
)
