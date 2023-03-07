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


from mailparser_reply import EmailReplyParser

from assistance._types import Email


def get_email_thread(email: Email):
    parser = EmailReplyParser()
    email_message = parser.read(email["plain_all_content"])
    email_thread = [str(item) for item in email_message.replies[-1::-1]]

    email_thread[-1] = f"On {email['date']}, {email['from']} wrote:\n{email_thread[-1]}"

    return email_thread
