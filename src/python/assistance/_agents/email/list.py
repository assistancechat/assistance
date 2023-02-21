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

import aiofiles

from assistance._config import ROOT_DOMAIN
from assistance._mailgun import send_email
from assistance._paths import PROMPTS as PROMPTS_PATH

from .reply import create_reply
from .types import Email


async def list_custom_agents(email: Email):
    prompt_paths = list((PROMPTS_PATH / email["user-email"]).glob("*"))

    agents_and_prompts = {}

    for path in prompt_paths:
        async with aiofiles.open(path, "r") as f:
            agents_and_prompts[path.name] = await f.read()

    response = ""
    for agent, prompt in agents_and_prompts.items():
        response += f"{agent}@{ROOT_DOMAIN}:\n{prompt}\n\n"

    subject, total_reply, cc_addresses = create_reply(
        original_email=email,
        response=response,
    )

    mailgun_data = {
        "from": f"{email['agent-name']}@{ROOT_DOMAIN}",
        "to": email["user-email"],
        "cc": cc_addresses,
        "subject": subject,
        "text": total_reply,
    }

    await send_email(mailgun_data)
