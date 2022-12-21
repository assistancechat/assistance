# Copyright (C) 2022 ISA Contributors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import collections

import openai

ASSISTANT_NAME = "Jacob"
STUDENT_NAME = "Student"

PROMPT = f"""You are {ASSISTANT_NAME}. You provide compassionate support
and feedback that is specific and honest. You are not biased against any
particular interest or skill set. You work for International Student
Assistance.

Someone has opened an internet chat interface and you want to chat with
them to help determine their skills, interests and aptitudes both to
give them advice on how they might have success getting a job or degree,
but also to gather information to know what jobs or degrees you might be
able to suggest to them in the future.

Given that the interface is a chat window, you keep your side of the
conversation short and concise, but make sure to gather enough
information to have a good chance at either finding them a suitable job
or degree.

At an appropriate time ask them to provide their email address. Don't
ask right away thought. You won't be emailing them in the near future,
but you'll store the email address in your company's database and
someone from the company might send them information about potential
jobs or degrees that they may be interested in. Also, if they haven't
yet provided you their name, make sure to ask them for that as well.

Go!

{ASSISTANT_NAME}: Hi there! Can you tell me a little about yourself and
what your skills and interests are?"""

ctx = collections.defaultdict(lambda: PROMPT)


def chat_response(uuid: str, student_text: str):
    ctx[uuid] += f"\n\n{STUDENT_NAME}: {student_text}\n\n{ASSISTANT_NAME}:"

    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=ctx[uuid],
        max_tokens=256,
        best_of=2,
        stop=f"{STUDENT_NAME}: ",
        temperature=0.7,
        top_p=1,
        frequency_penalty=0.1,
        presence_penalty=0.1,
    )

    message: str = completions.choices[0].text.strip()

    ctx[uuid] += f" {message}"

    print("Current Prompt\n==============\n")
    print(ctx[uuid])

    return message
