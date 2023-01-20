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

import logging
import textwrap

import openai

MODEL_KWARGS = {
    "engine": "text-davinci-003",
    "max_tokens": 256,
    "best_of": 2,
    "temperature": 0.7,
    "top_p": 1,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
}

PROMPT = textwrap.dedent(
    """
        Write a search engine query that helps provide extra
        information to Michael to help him provide his next response.

        Keep the query broad.

        Transcript:
        {transcript}

        Question:
    """
).strip()


async def query_from_transcript(record_grouping: str, username: str, transcript: str):
    prompt = PROMPT.format(transcript=transcript)

    completions = await openai.Completion.acreate(prompt=prompt, **MODEL_KWARGS)
    response: str = completions.choices[0].text.strip().replace('"', "")

    logging.info(f"Query: {response}")

    return response
