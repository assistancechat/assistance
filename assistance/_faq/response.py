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

import asyncio
import json
import re
import textwrap
from datetime import datetime
from zoneinfo import ZoneInfo

from mailparser_reply import EmailReplyParser

from assistance import _ctx
from assistance._config import DEFAULT_OPENAI_MODEL, ROOT_DOMAIN, load_faq_data
from assistance._email.reply import create_reply, get_all_user_emails
from assistance._email.thread import get_email_thread
from assistance._embeddings import get_top_questions_and_answers
from assistance._keys import get_openai_api_key, get_serp_api_key
from assistance._logging import log_info
from assistance._mailgun import send_email
from assistance._openai import get_completion_only
from assistance._summarisation.thread import run_with_summary_fallback
from assistance._tooling.executive_function_system import get_tools_and_responses
from assistance._types import Email
from assistance._utilities import get_cleaned_email, items_to_list_string

from .answer import write_answer
from .correspondent import get_first_name
from .extract_questions import extract_questions

OPEN_AI_API_KEY = get_openai_api_key()
SERP_API_KEY = get_serp_api_key()

MODEL_KWARGS = {
    "engine": DEFAULT_OPENAI_MODEL,
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}


PROMPT = textwrap.dedent(
    """
        # Write an email introduction and conclusion

        You have been forwarded an email from Alex Carpenter.
        {students_name}, a prospective student is asking him questions
        about Jim's International Pathway Program. You are happy to help
        answer any questions that the prospective student may have about
        the Jim's International Pathway Program.

        You have been provided with a list of the answers to a range of
        questions that the prospective student asked. You are to write
        the introduction to the email response and the conclusion to the
        email response.

        This introduction and conclusion will be prepended and appended
        around the question answers that you have already been provided.

        DO NOT include the question and answers within your introduction
        or your conclusion.

        The name to sign the email with is "Alex Carpenter".

        ## The questions and their answers that you have been provided.

        You do not need to repeat these. They will already be included
        within your email response.

        {question_and_answers}

        ## Email transcript

        {transcript}

        ## Required JSON format

        {{
            "introduction": "<Your email introduction>",
            "conclusion": "<Your email conclusion>"
        }}

        ## Your JSON response (ONLY respond with JSON, nothing else)
    """
).strip()


async def write_and_send_email_response(
    faq_name: str,
    email: Email,
):
    scope = email["user_email"]
    faq_data = await load_faq_data(faq_name)

    email_thread = get_email_thread(email=email)

    if email["subject"].startswith("Fwd: ") or email["subject"].startswith("FW: "):
        subject = email["subject"].removeprefix("Fwd: ").removeprefix("FW: ")

        last_message_lower = email_thread[-1].lower()

        first_reply_line = email["plain_replies_only"].splitlines()[0]
        if first_reply_line.startswith("From: "):
            reply_to = get_cleaned_email(first_reply_line)

        else:
            try:
                reply_to = get_cleaned_email(
                    last_message_lower.split("forwarded message")[-1]
                )
            except ValueError:
                reply_to = email["from"]
    else:
        reply_to = email["from"]
        subject = None

    students_name = await get_first_name(
        scope=scope, email_thread=email_thread, their_email_address=reply_to
    )

    questions_and_contexts = await extract_questions(email=email)

    coroutines = []
    for question_and_context in questions_and_contexts:
        coroutines.append(
            write_answer(
                scope=scope,
                faq_data=faq_data,
                question_and_context=question_and_context,
            )
        )

    answers = await asyncio.gather(*coroutines)

    question_and_answers_string = ""
    for question_and_context, answer in zip(questions_and_contexts, answers):
        question_and_answers_string += (
            f"Q: {question_and_context['question']}\nA: {answer}\n\n"
        )

    question_and_answers_string = question_and_answers_string.strip()

    prompt = PROMPT.format(
        transcript="{transcript}",
        question_and_answers=question_and_answers_string,
        students_name=students_name,
    )

    response = await run_with_summary_fallback(
        scope=scope,
        prompt=prompt,
        email_thread=email_thread,
        api_key=OPEN_AI_API_KEY,
        **MODEL_KWARGS,
    )

    log_info(scope, response)

    result = json.loads(response)
    response_email = f"{result['introduction'].strip()}\n\n{question_and_answers_string}\n\n{result['conclusion'].strip()}"

    reply = create_reply(original_email=email, response=response_email)
    if subject is None:
        subject = reply["subject"]

    mailgun_data = {
        "from": f"{faq_name}-faq@{ROOT_DOMAIN}",
        "to": ["alexcarpenter2000@gmail.com"],
        "cc": ["me@simonbiggs.net"],
        "reply_to": reply_to,
        "subject": subject,
        "html_body": reply["html_reply"],
    }

    await send_email(scope, mailgun_data)
