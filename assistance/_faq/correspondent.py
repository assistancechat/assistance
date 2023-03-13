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

import textwrap

from assistance._config import DEFAULT_OPENAI_MODEL
from assistance._keys import get_openai_api_key
from assistance._summarisation.thread import run_with_summary_fallback

OPEN_AI_API_KEY = get_openai_api_key()

MODEL_KWARGS = {
    "engine": DEFAULT_OPENAI_MODEL,
    "max_tokens": 256,
    "temperature": 0.7,
    "stop": ["\n"],
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}


PROMPT = textwrap.dedent(
    """
        # Get Correspondent

        Alex Carpenter is having an email conversation with a
        prospective student who's email address is {email_address}. What
        is the first name of this student?

        ## Email transcript

        {transcript}

        ## Response

        First Name:
    """
).strip()


async def get_first_name(scope: str, email_thread, their_email_address: str) -> str:
    prompt = PROMPT.replace("{email_address}", their_email_address)
    response = await run_with_summary_fallback(
        scope=scope,
        prompt=prompt,
        email_thread=email_thread,
        api_key=OPEN_AI_API_KEY,
        **MODEL_KWARGS,
    )

    return response
