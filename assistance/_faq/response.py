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

from assistance._config import load_faq_data
from assistance._embeddings import get_top_questions_and_answers_text
from assistance._keys import get_openai_api_key


import json
import re
import textwrap
from datetime import datetime
from zoneinfo import ZoneInfo

from mailparser_reply import EmailReplyParser

from assistance import _ctx
from assistance._openai import get_completion_only
from assistance._config import DEFAULT_OPENAI_MODEL, ROOT_DOMAIN
from assistance._email.reply import create_reply, get_all_user_emails
from assistance._email.thread import get_email_thread
from assistance._keys import get_openai_api_key, get_serp_api_key
from assistance._logging import log_info
from assistance._mailgun import send_email
from assistance._summarisation.thread import run_with_summary_fallback
from assistance._tooling.executive_function_system import get_tools_and_responses
from assistance._types import Email
from assistance._config import load_faq_data
from .queries import get_queries
from assistance._utilities import items_to_list_string
from assistance._utilities import get_cleaned_email


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


EMAIL_PROMPT = textwrap.dedent(
    """
        {task}

        ## Tool results

        {tool_results}

        ## Your email response (email content ONLY)
    """
).strip()


TASK = textwrap.dedent(
    """
        ## Overview

        You have been forwarded an email from Alex Carpenter. A
        prospective student is asking him questions about Jim's
        International Pathway Program. You are happy to help answer any
        questions that the prospective student may have about the Jim's
        International Pathway Program.

        You are to draft Alex's response for him. Below are a range of
        previous FAQ responses that Alex has provided to other students.
        Use these FAQ responses as a guide to help you draft your own
        response.

        You have also been provided with a range of tool results. Use
        these tool results to help you draft your own response.

        ## Questions asked by THIS applicant

        {queries}

        ## Previous responses to OTHER prospective students

        These questions are not necessarily the same as the questions
        asked by this prospective student. However, you may use the
        responses to these questions as a guide to help you draft your
        own response.

        {faq_responses}

        ## Instructions

        - Ask open-ended questions to understand what their needs are
        - Show genuine empathy and interest in their situation
        - DO NOT utilise any of your outside knowledge to fill in any
          gaps. Instead only utilise the tool results and FAQ responses
          to help you draft your response.

        ## Details about the email record

        - The subject of the email thread is "{subject}".

        ## Email transcript

        {transcript}
    """
).strip()


async def write_and_send_email_response(
    faq_name: str,
    email: Email,
):
    scope = email["user_email"]
    faq_data = await load_faq_data("jims-ac")
    queries = await get_queries(email=email)

    faq_responses = await get_top_questions_and_answers_text(
        openai_api_key=OPEN_AI_API_KEY, faq_data=faq_data, queries=queries
    )

    task = TASK.format(
        subject=email["subject"],
        transcript="{transcript}",
        queries=items_to_list_string(queries),
        faq_responses=faq_responses,
    )

    email_thread, prompt = await _get_prompt(email, task)

    log_info(scope, _ctx.pp.pformat(email_thread))

    response = await run_with_summary_fallback(
        scope=scope,
        prompt=prompt,
        email_thread=email_thread,
        api_key=OPEN_AI_API_KEY,
        **MODEL_KWARGS,
    )

    log_info(scope, response)

    reply = create_reply(original_email=email, response=response)

    if email["subject"].startswith("Fwd: "):
        reply["subject"] = email["subject"][5:]

        last_message_lower = email_thread[-1].lower()

        try:
            reply_to = get_cleaned_email(
                last_message_lower.split("forwarded message")[-1]
            )
        except ValueError:
            reply_to = email["from"]
    else:
        reply_to = email["from"]

    mailgun_data = {
        "from": f"{faq_name}-faq@{ROOT_DOMAIN}",
        "to": ["alexcarpenter2000@gmail.com"],
        "cc": ["me@simonbiggs.net"],
        "reply_to": reply_to,
        "subject": reply["subject"],
        "html_body": reply["html_reply"],
    }

    await send_email(scope, mailgun_data)


EXAMPLE_TOOL_USE = textwrap.dedent(
    """
        [
            {{
                "id": 0,
                "step_by_step_thought_process": "I will start by using the 'now' tool to get the current date and time.",
                "tool": "now",
                "args": [],
                "score": 9,
                "confidence": 8
            }},
            {{
                "id": 1,
                "step_by_step_thought_process": "I am going to search for more details about the courses at Alphacrucis.",
                "tool": "internet_search",
                "args": ["Courses at Alphacrucis University"],
                "score": 9,
                "confidence": 8
            }}
        ]
    """
).strip()


EXTRA_TOOLS = ""


async def _get_prompt(email: Email, task: str):
    scope = email["user_email"]

    email_thread = get_email_thread(email)

    log_info(scope, json.dumps(email_thread, indent=2))

    tools = await get_tools_and_responses(
        scope=scope,
        task=task,
        email_thread=email_thread,
        example_tool_use=EXAMPLE_TOOL_USE,
        extra_tools=EXTRA_TOOLS,
    )
    keys_to_keep = ["step_by_step_thought_process", "tool", "args", "result"]

    filtered_tools = []
    for tool in tools:
        filtered_tool = {key: tool[key] for key in keys_to_keep}
        filtered_tools.append(filtered_tool)

    tools_string = json.dumps(filtered_tools, indent=2)

    prompt = EMAIL_PROMPT.format(
        task=task, tool_results=tools_string, transcript="{transcript}"
    )

    return email_thread, prompt
