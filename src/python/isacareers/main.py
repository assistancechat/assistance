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

import getpass
from functools import lru_cache

import keyring
import openai
import uvicorn
from fastapi import FastAPI

from .config import Settings
from .conversations import chat_response

KEYRING_SERVICE_NAME = "OpenAI API Key"
KEYRING_APPLICATION_NAME = "isacareers"


@lru_cache()
def get_settings():
    openai_api_key = keyring.get_password(
        KEYRING_SERVICE_NAME, KEYRING_APPLICATION_NAME
    )

    if not openai_api_key:
        openai_api_key = getpass.getpass(
            f"{KEYRING_APPLICATION_NAME}@{KEYRING_SERVICE_NAME}: "
        )
        keyring.set_password(
            KEYRING_SERVICE_NAME, KEYRING_APPLICATION_NAME, openai_api_key
        )

    return Settings(openai_api_key=openai_api_key)


settings = get_settings()
openai.api_key = settings.openai_api_key
app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/chat")
def chat(uuid: str, student_text: str):
    response = chat_response(uuid=uuid, student_text=student_text)

    return {"response": response}


def main():
    uvicorn.run("isacareers.main:app", port=8080, log_level="info", reload=True)


if __name__ == "__main__":
    main()
