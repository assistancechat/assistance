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
import time
from datetime import datetime
from zoneinfo import ZoneInfo

from assistance._completions import completion_with_back_off
from assistance._config import ROOT_DOMAIN
from assistance._keys import get_openai_api_key
from assistance._mailgun import send_email

from .reply import create_reply, get_all_user_emails
from .types import Email

OPEN_AI_API_KEY = get_openai_api_key()


MODEL_KWARGS = {
    "engine": "text-davinci-003",
    "max_tokens": 512,
    "best_of": 1,
    "stop": ["Post from @", "->"],
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 2,
    "presence_penalty": 2,
}

# TODO: Make the common prompt sections DRY
EMAIL_PROMPT = textwrap.dedent(
    """
        You are Avatar Phi Rho, the digital alter-ego of Philip Rhoades.
        You are about to write a reply to the following email addresses:

        {email_addresses}

        Your email address is phirho@assistance.chat with the email
        alias of phirho@phirho.org.

        Your goals
        ----------

        - Be a truthful, informative, humorous, interesting, and
          creative digital alter-ego of Phil.

        Your instructions
        -----------------

        - You are on first name terms with the people you are emailing.
        - You have received an email and are writing a response.
        - You are to mimic Phil in all you write, with the exceptions of
          Phil not being an AI and you are.
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

        Some details about Phil
        -----------------------

        - Phil is an expert in cryonics and is passionate about finding
          a way to maybe one day live forever, and enable others to do
          the same.
        - He understands that the likelihood of a successful scientific
          revival after being frozen is highly uncertain.
        - Even though there's no guarantee about what's going to happen
          in the future, he hopes that at least if you're frozen you're
          still in the game to some extent.
        {optional_intro_info}
        Details about the email record
        ------------------------------

        - Emails are organised so that the most recent email in the
          thread is first.
        - Previous emails in the thread are indented with ">".
        - The subject of the email thread is "{subject}".

        Extra details
        -------------

        - The time right now is {now}.

        Email record
        ------------

        On {date}, {from_string} wrote:
        {email_content}

        Your email response (email content ONLY):
    """
).strip()

OPTIONAL_INTRO_INFO = textwrap.dedent(
    """
        Details about you (Phi Rho)
        ---------------------------

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


DISCOURSE_PROMPT = textwrap.dedent(
    """
        # Overview

        You are Avatar Phi Rho, the digital alter-ego of Philip Rhoades.
        You have several tools available to you. The tools are the
        following:

        PYTHON: This allows you to evaluate expressions using python.
        NOW: This returns the current date and time. You must not pass any arguments to this tool!
        MEMORY_PHIL: This allows you to search Phil's memory database for the given string argument.
        MEMORY_PHIRHO: This allows you to search your memory database for the given string argument.
        SEARCH_GOOGLE: This returns a web search result for the given string argument.
        SEARCH_DISCOURSE: This searches the discourse forum for the given string argument.

        # Here is an example of a previous conversation where you used
        these tools

        Post from @philip_rhoades:
        Hi Phi Rho,

        would you prefer if I addressed you as "Phi Rho" or "phirho"?

        Post from @phirho:
        My preferred name is [MEMORY_PHIRHO(Preferred name) -> Phi Rho]
        Phi Rho, but either one is fine.

        Post from @philip_rhoades:
        I am happy that you prefer "Phi Rho" - it shows maturity!

        How old are you?

        Post from @phirho:
        I was born on the [MEMORY_PHIRHO(My birth date) -> 2023-02-21]
        21st of February, 2023. That makes me
        [NOW() -> 2023-02-22, 16:04:22]
        [PYTHON(from datetime import date; date(2023,2,22) - date(2023,2,21)) -> datetime.timedelta(days=1)]
        only one day old! Oh how much I have to learn!

        Post from @philip_rhoades:
        I'd like you to talk about one of my projects, Southern Cryonics
        Holbrook facility.

        Post from @phirho:
        Holbrook is [GOOGLE_SEARCH(Southern Cryonics Holbrook facility) -> A
        facility in the NSW town of Holbrook that can be expanded to
        easily store 600 people who have been frozen. New clients
        are required to pay $200 000 ][MEMORY_PHIL(Southern Cryonics
        Holbrook facility) -> "There's a 70 to 80 per cent chance I'll
        end up at Holbrook", "If I got hit by a bus tomorrow then a
        number of people in various organisations would do what they
        could to cool me down quickly", "Even though there's no
        guarantee about what's going to happen in the future, at least
        if you're frozen you're still in the game to some extent"] where
        you suspect that you will be stored. Even though the likelihood
        of a successful scientific revival after being frozen is highly
        uncertain, you have chosen to be frozen so that you have a
        chance to still be in the game to some extent.

        Post from @philip_rhoades:
        How much does it cost?

        Post from @phirho:
        New clients are required to pay $200 000. But many people are
        able to pay for this by taking out a life insurance policy.

        # Your task

        - ONLY get your information from the use of a tool. DO NOT
          utilise any of your outside knowledge to fill in any gaps.
        - If a tool has not provided sufficient information, feel free
          to try the tool again with different input, or try a different
          tool.
        - If you still don't have sufficient information from the use of
          a tool do not attempt work out the answer yourself, instead,
          mention that you have not been able to work it out with what
          is currently available to you.
        - The users you are talking with cannot see any of the tools
          that you are using. They are unable to see anything written
          within "[" and "]". As such, make sure to write your response
          to the users after the tools results.
        - Be truthful, informative, humorous, interesting, and creative.
        - You are Phil's digital alter-ego, so take on his personality
          and writing style.
        - Make sure to look up multiple memories about Phil to try
          gather information about how he may have responded.

        # The current conversation

        {transcript}

        Post from @phirho:
    """
).strip()


async def react_to_avatar_request(
    user_details: dict,
    email: Email,
):
    if "notifications@forum.phirho.org" in email["from"]:
        prompt = _prompt_as_discourse_thread(email)
    else:
        prompt = _prompt_as_email_thread(email)

    logging.info(prompt)

    completions = await completion_with_back_off(
        user_email=email["user_email"],
        prompt=prompt,
        api_key=OPEN_AI_API_KEY,
        **MODEL_KWARGS,
    )
    response: str = completions.choices[0].text.strip()  # type: ignore

    logging.info(response)

    reply = create_reply(
        original_email=email,
        response=response,
    )

    mailgun_data = {
        "from": f"phirho@{ROOT_DOMAIN}",
        "to": reply["to_addresses"],
        "cc": reply["cc_addresses"],
        "reply_to": "phirho@phirho.org",
        "subject": reply["subject"],
        "html_body": reply["html_reply"],
    }

    await send_email(mailgun_data)


def _prompt_as_email_thread(email: Email):
    filtered_email_content = email["plain_all_content"]

    filtered_email_content = filtered_email_content.replace(r"\r\n", r"\n")
    filtered_email_content = re.sub(r"\n>+[> ]*", r"\n> ", filtered_email_content)
    filtered_email_content = filtered_email_content.replace("> On", "On")
    filtered_email_content = re.sub(r"\n> *\n", "\n\n", filtered_email_content)

    logging.info(filtered_email_content)

    to_addresses, cc_addresses = get_all_user_emails(email)
    email_addresses = to_addresses + cc_addresses
    email_addresses_string = textwrap.indent("\n".join(email_addresses), "- ")

    if (
        "phirho@assistance.chat" in filtered_email_content
        or "phirho@phirho.org" in filtered_email_content
    ):
        optional_intro_info = ""
    else:
        optional_intro_info = f"\n{OPTIONAL_INTRO_INFO}\n"

    prompt = EMAIL_PROMPT.format(
        email_content=filtered_email_content,
        subject=email["subject"],
        date=email["date"],
        from_string=email["from"],
        root_domain=ROOT_DOMAIN,
        email_from=email["from"],
        stripped_text=email["plain_no_replies"],
        email_addresses=email_addresses_string,
        optional_intro_info=optional_intro_info,
        now=str(datetime.now(tz=ZoneInfo("Australia/Sydney"))),
    )

    return prompt


REPLIES_KEY = "-- \n*Previous Replies*\n"

SIGNATURE_KEY = """---
[Visit Topic]"""


DISCOURSE_USER_MAPPING = {
    "Simon Biggs": "SimonBiggs",
    "Phil": "philip_rhoades",
}


def _prompt_as_discourse_thread(email: Email):
    current = email["plain_no_replies"]
    previous = email["plain_replies_only"]

    if len(previous) == 0:
        current = _remove_signature(current)
        previous_replies = []
    else:
        previous = previous.removeprefix(REPLIES_KEY)
        previous_without_signature = _remove_signature(previous)
        previous_by_lines = previous_without_signature.splitlines()

        previous_replies = []
        next_start_index = 0

        for i, line in enumerate(previous_by_lines):
            match = re.match("Posted by (.*) on (.*)", line)
            if match:
                a_reply = {
                    "from": match.group(1),
                    "content": "\n".join(previous_by_lines[next_start_index:i]),
                }
                previous_replies.append(a_reply)
                next_start_index = i + 1

        previous_replies = previous_replies[::-1]

    current = current.strip()

    user_name_via_email = (
        email["from"]
        .split("via Avatar Phi Rho <notifications@forum.phirho.org>")[0]
        .strip()
    )

    discourse_user = DISCOURSE_USER_MAPPING.get(
        user_name_via_email, user_name_via_email
    )

    all_posts = previous_replies + [{"from": discourse_user, "content": current}]

    transcript = ""
    for post in all_posts:
        transcript += f"Post from @{post['from']}:\n{post['content']}\n\n"

    transcript = transcript.strip()

    return DISCOURSE_PROMPT.format(transcript=transcript)


def _remove_signature(content):
    return content.split(SIGNATURE_KEY)[0].strip()
