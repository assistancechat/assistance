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

# Prompt inspired by the work provided under an MIT license over at:
# https://github.com/hwchase17/langchain/blob/ae1b589f60a/langchain/agents/conversational/prompt.py#L1-L36


from .types import Email


def create_reply(original_email: Email, response: str):
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

    return subject, total_reply
