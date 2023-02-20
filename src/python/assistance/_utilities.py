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
from urllib.parse import parse_qs, urlparse

WORDS_PER_TOKEN = 0.75
APPROXIMATE_ALLOWED_WORDS_IN_PROMPT = 4097 * WORDS_PER_TOKEN


def items_to_list_string(items):
    return textwrap.indent("\n".join(items), "- ")


def get_approximate_allowed_remaining_words(prompt: str, max_tokens: int):
    words_in_prompt = get_number_of_words(prompt)
    num_words_used_by_tokens = max_tokens * WORDS_PER_TOKEN

    return APPROXIMATE_ALLOWED_WORDS_IN_PROMPT - (
        num_words_used_by_tokens + words_in_prompt
    )


def get_number_of_words(text: str):
    return len(text.split(None))


def get_cleaned_url(url: str):
    parsed_url = urlparse(url)
    cleaned_url = parse_qs(parsed_url.query)["url"][0]

    return cleaned_url
