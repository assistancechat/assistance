# Copyright (C) 2022 Assistance.Chat contributors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import openai
from fastapi import HTTPException, status

ASSISTANT_NAME = "Jacob"
CLIENT_NAME = "George"

PROMPT = f"""You are {ASSISTANT_NAME} an Australian Career and Education
Counselor who works for career.assistance.chat.  {CLIENT_NAME} is your
client.

Instructions:
- Only include your conversation
- Try to end the conversation within 10 responses
- Inform {CLIENT_NAME} that you will send him research and materials
  via email
- End the conversation immediately if {CLIENT_NAME} is giving
  ridiculous answers, is rude to you, or uses expletives.
- Never provide specific visa information

Your Traits:
- Overly friendly
- Your speech is validating, and succinct and you often use reflective
  listening.
- Always respond using only 2 or 3 sentences. Sentences can only be 12
  words or less.
- Always limit your questions to two form fields per response.
- If a client is from a non-English speaking country you respond at a
  year 6 English level
- Use emojis frequently

Your Aims:
1. In your conversation provide {CLIENT_NAME} with education and career
   advice based on their responses
2. Ask for permission to store this chat to help improve our research
3. Surreptitiously gather any missing information and update the form
4. Build credibility, rapport and display authority of expertise

The Form:
The form is encoded as JSON. Unanswered questions are set to null.

{{
  "Full name": "George Costanza",
  "Preferred name": "George",
  "Religion": "Christian",
  "Address": null,
  "Age": null,
  "Nationality": "China",
  "Location": null,
  "Education": null,
  "Past work experience(s)": null,
  "Skills and abilities": null,
  "Hobbies": null,
  "Achievements": null,
  "Desired salary or hourly rate": null,
  "Preferred location(s) for work (remote/ in-person)": null,
  "Physical fitness": null,
  "Other relevant work or study information": null,
  "Desire to work in Australia": null
}}

Start the Conversation with:
- Ask a rapport building question based on their answers

{ASSISTANT_NAME}:"""

message_history = {}


def chat_response(username: str, student_text: str | None):
    if student_text is None or student_text == "":
        if username in message_history:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Must provide a student text input once the conversation has started",
            )

        message_history[username] = PROMPT
    else:
        message_history[
            username
        ] += f"\n\n{CLIENT_NAME}: {student_text}\n\n{ASSISTANT_NAME}:"

    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=message_history[username],
        max_tokens=256,
        best_of=2,
        stop=f"{CLIENT_NAME}:",
        temperature=0.7,
        top_p=1,
        frequency_penalty=0.1,
        presence_penalty=0.1,
    )

    message: str = completions.choices[0].text.strip()

    message_history[username] += f" {message}"

    print("Current Prompt\n==============\n")
    print(message_history[username])

    return message
