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


from html import escape

from .types import Email

ALIASES = {"phirho@phirho.org": "avatar"}


def create_reply(
    original_email: Email,
    response: str,
    additional_cc_addresses: list[str] | None = None,
):
    subject = original_email["subject"]

    if not subject.startswith("Re:"):
        subject = f"Re: {subject}"

    body_plain = original_email["body-plain"]
    date = original_email["Date"]

    email_lines = body_plain.strip().splitlines()
    if len(email_lines[-1]) == 0:
        email_lines = email_lines[:-1]

    quoted_lines = []
    for line in email_lines:
        if line.startswith(">"):
            quoted_lines.append(f">{line}")
        else:
            quoted_lines.append(f"> {line}")

    previous_email_with_indent = "\n".join(quoted_lines)

    previous_emails = (
        f"On {date}, {original_email['from']} wrote:\n{previous_email_with_indent}"
    )

    total_reply = f"{response}\n\n{previous_emails}"

    response_as_html = _convert_text_to_html(response)
    html_attribution = escape(f"On {date}, {original_email['from']} wrote:")

    try:
        original_email_body_html = original_email["body-html"]
    except KeyError:
        original_email_body_html = _convert_text_to_html(original_email["body-plain"])

    html_reply = (
        f'<div dir="ltr">{response_as_html}</div><br>'
        '<div class="gmail_quote"><div dir="ltr" class="gmail_attr">'
        f'{html_attribution}<br></div><blockquote class="gmail_quote"'
        'style="margin:0px 0px 0px 0.8ex;border-left:1px solid '
        f'rgb(204,204,204);padding-left:1ex">{original_email_body_html}'
        "</blockquote></div>"
    )

    aliases_removed = get_all_cc_user_emails(original_email, additional_cc_addresses)

    cc_addresses = ", ".join(aliases_removed)

    return subject, total_reply, cc_addresses, html_reply


def _convert_text_to_html(text: str):
    return (
        escape(text).replace("\r\n", "\n").replace("\n", "<br>").replace("\r", "<br>")
    )


def get_all_cc_user_emails(email: Email, extra: list[str] | None = None):
    if extra is not None:
        all_possible_cc_addresses = extra
    else:
        all_possible_cc_addresses = []

    try:
        all_possible_cc_addresses += email["Cc"].split(",")
    except KeyError:
        pass

    try:
        all_possible_cc_addresses += email["Sender"].split(",")
    except KeyError:
        pass

    try:
        all_possible_cc_addresses += email["To"].split(",")
    except KeyError:
        pass

    stripped_cc_addresses = [item.strip() for item in all_possible_cc_addresses]
    no_overlap_cc_addresses = [
        item for item in set(stripped_cc_addresses) if not email["user-email"] in item
    ]

    no_assistance_chat_cc_addresses = [
        item for item in no_overlap_cc_addresses if not "assistance.chat" in item
    ]

    aliases_removed = no_assistance_chat_cc_addresses
    for an_alias in ALIASES.keys():
        aliases_removed = [item for item in aliases_removed if not an_alias in item]

    return aliases_removed
