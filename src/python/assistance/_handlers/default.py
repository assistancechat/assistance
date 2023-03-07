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

from assistance._config import ROOT_DOMAIN
from assistance._forms.response import react_to_enrolment_request
from assistance._news.pipeline import add_to_google_alerts_pipeline

DEFAULT_TASKS = {
    "enrolment": ("", react_to_enrolment_request),
    "googlealerts": (
        "Stores a Google Alert for future use by the targeted-news agent.",
        add_to_google_alerts_pipeline,
    ),
    "poem-demo": (
        "This is an example assistant who responds with a poem",
        "Respond to email with a beautiful and relevant poem",
    ),
    "sales-demo": (
        "This is an example sales assistant who is trying to sell you water",
        "Respond to email with a sales pitch for water. You are trying to sell the user water.",
    ),
    "bible-demo": (
        "An AI bot that gives a relevant bible verse. ",
        "Make sure to quote both the verse and the reference. "
        "Give some details about the context and maybe even the meaning "
        "of some of the words in the original language if it might help "
        "in understanding.",
    ),
}

_task_overviews = ""
for agent, (overview, _prompt) in DEFAULT_TASKS.items():
    _task_overviews += f"- {agent}@{ROOT_DOMAIN}: {overview}\n"


HI_PROMPT = (
    textwrap.dedent(
        """
            You are the user's first port of call to using {ROOT_DOMAIN}.
            You are to have a welcoming discussion with them and provide
            them with an overview of what can be done.

            Overview of the AI agent emails and what they can do:
            {task_overviews}
        """
    )
    .format(task_overviews=_task_overviews, ROOT_DOMAIN=ROOT_DOMAIN)
    .strip()
)


DEFAULT_TASKS["hi"] = ("Used to onboard new users", HI_PROMPT)
