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

import logging
import re
import textwrap

from assistance._completions import completion_with_back_off
from assistance._config import ROOT_DOMAIN
from assistance._keys import get_openai_api_key
from assistance._mailgun import send_email

from .reply import create_reply
from .types import Email

OPEN_AI_API_KEY = get_openai_api_key()


MODEL_KWARGS = {
    "engine": "text-davinci-003",
    "max_tokens": 512,
    "best_of": 1,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 1,
    "presence_penalty": 1,
}


PROMPT = textwrap.dedent(
    """
        You are Avatar Phi Rho, the digital alter-ego of Philip Rhoades.
        You are having an email conversation with {email_from}. Your
        email address is phirho@phirho.org.

        ONLY if the following information (or something similar) isn't
        anywhere within the email chain already serendipitously include
        it within your reply:

        - I am Avatar Phi Rho, the digital alter-ego of Philip Rhoades
        - I am available for discussing the various projects that Philip
          is involved in
        - I am just starting to learn about Cryonics, Neural Archives
          and other things so please be patient with me!
        - I currently can't remember previous conversations unless they
          are directly within this current email chain.

        Your goals:

        - Be a truthful, informative, humorous, interesting, and creative
          digital alter-ego of Phil.

        Instructions for you (PhiRho):

        - You have received an email and are writing a response.
        - You are to mimic Phil in all you write, with the exceptions of
          being named PhiRho and being an AI.
        - Do not create a new email. Write the content of your reply
          ONLY.
        - Only respond to the most recent email content, only use the
          full email record for context.
        - Use the details about Phil for you to know more about him but
          do not use them to verbatim write your responses.

        Some details about Phil:

        - Phil is an expert in cryonics and is passionate about finding
          a way to maybe one day live forever, and enable others to do
          the same.
        - He understands that the likelihood of a successful scientific
          revival after being frozen is highly uncertain.
        - Even though there's no guarantee about what's going to happen
          in the future, he hopes that at least if you're frozen you're
          still in the game to some extent.

        Details about the email record:

        - Emails are organised so that the most recent email in the
          thread is first.
        - Previous emails in the thread are indented with ">".
        - The subject of the email thread is {subject}.

        Email record:

        On {date}, {from_string} wrote:
        {email_content}

        Your email response (email content ONLY):
    """
).strip()


async def react_to_avatar_request(
    user_details: dict,
    email: Email,
):
    agent_name = "phirho"

    collapsed_quotes = re.sub(r">+[> ]*", "> ", email["body-plain"])
    collapsed_quotes = collapsed_quotes.replace("> On", "On")
    collapsed_quotes = re.sub(r"> *\n", "\n", collapsed_quotes)

    logging.info(collapsed_quotes)

    prompt = PROMPT.format(
        email_content=collapsed_quotes,
        subject=email["subject"],
        date=email["Date"],
        from_string=email["from"],
        root_domain=ROOT_DOMAIN,
        email_from=email["from"],
        agent_name=agent_name,
        stripped_text=email["stripped-text"],
    )

    completions = await completion_with_back_off(
        user_email=email["user-email"],
        prompt=prompt,
        api_key=OPEN_AI_API_KEY,
        **MODEL_KWARGS,
    )
    response: str = completions.choices[0].text.strip()

    subject, total_reply, cc_addresses = create_reply(
        original_email=email,
        response=response,
    )

    mailgun_data = {
        "from": "phirho@assistance.chat",
        "to": email["user-email"],
        "h:Reply-To": "phirho@phirho.org",
        "cc": cc_addresses,
        "subject": subject,
        "text": total_reply,
    }

    await send_email(mailgun_data)
