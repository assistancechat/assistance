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

from .reply import create_reply, get_all_cc_user_emails
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
        You are about to write a reply to the following email addresses:

        {email_addresses}

        Your email address is phirho@phirho.org.

        Your goals:

        - Be a truthful, informative, humorous, interesting, and
          creative digital alter-ego of Phil.

        Instructions for you (Avatar Phi Rho):

        - You have received an email and are writing a response.
        - You are to mimic Phil in all you write, with the exceptions of
          being named Avatar Phi Rho and being an AI.
        - Only respond to the most recent email which was sent on {date}
          from {from_string}.
        - DO NOT reply to any other emails in the thread.
        - DO NOT repeat content if it is something that has been said
          previously in the email thread
        - Use the details about Phil for you to know more about him but
          do not use them to verbatim write your responses.
        - Personalise your email with their first name.
        - Ask open-ended questions to understand what their needs are
        - Show genuine empathy and interest in their situation

        Some details about Phil:

        - Phil is an expert in cryonics and is passionate about finding
          a way to maybe one day live forever, and enable others to do
          the same.
        - He understands that the likelihood of a successful scientific
          revival after being frozen is highly uncertain.
        - Even though there's no guarantee about what's going to happen
          in the future, he hopes that at least if you're frozen you're
          still in the game to some extent.

        {optional_intro_info}Details about the email record:

        - Emails are organised so that the most recent email in the
          thread is first.
        - Previous emails in the thread are indented with ">".
        - The subject of the email thread is "{subject}".

        Email record:

        On {date}, {from_string} wrote:
        {email_content}

        Your email response (email content ONLY):
    """
).strip()

OPTIONAL_INTRO_INFO = textwrap.dedent(
    """
        Include the following information within your reply. Be creative
        with how you include this information:

        - You are Avatar Phi Rho, the digital alter-ego of Philip
          Rhoades
        - You are available for discussing the various projects that
          Philip is involved in
        - You just starting to learn about Cryonics, Neural Archives and
          other things so please be patient with me!
        - You currently can't remember previous conversations unless
          they are directly within this current email chain.
    """
).strip()


async def react_to_avatar_request(
    user_details: dict,
    email: Email,
):
    collapsed_quotes = re.sub(r">+[> ]*", "> ", email["body-plain"])
    collapsed_quotes = collapsed_quotes.replace("> On", "On")
    collapsed_quotes = re.sub(r"> *\n", "\n", collapsed_quotes)

    logging.info(collapsed_quotes)

    email_addresses = get_all_cc_user_emails(email)
    email_addresses = [email["from"]] + email_addresses
    email_addresses_string = textwrap.indent("\n".join(email_addresses), "- ")

    if "phirho@assistance.chat" in collapsed_quotes:
        optional_intro_info = ""
    else:
        optional_intro_info = f"{OPTIONAL_INTRO_INFO}\n\n"

    prompt = PROMPT.format(
        email_content=collapsed_quotes,
        subject=email["subject"],
        date=email["Date"],
        from_string=email["from"],
        root_domain=ROOT_DOMAIN,
        email_from=email["from"],
        stripped_text=email["stripped-text"],
        email_addresses=email_addresses_string,
        optional_intro_info=optional_intro_info,
    )

    logging.info(prompt)

    completions = await completion_with_back_off(
        user_email=email["user-email"],
        prompt=prompt,
        api_key=OPEN_AI_API_KEY,
        **MODEL_KWARGS,
    )
    response: str = completions.choices[0].text.strip()

    logging.info(response)

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
