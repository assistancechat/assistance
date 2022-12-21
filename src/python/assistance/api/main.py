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


import uvicorn
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from .conversations import chat_response
from .keys import set_openai_api_key

app = FastAPI()

set_openai_api_key()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    uuid: str
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    disabled: bool | None = None


@app.post("/chat")
def chat(uuid: str, student_text: str, token: str = Depends(oauth2_scheme)):
    response = chat_response(uuid=uuid, student_text=student_text)

    return {"response": response}


def main():
    uvicorn.run("assistance.api.main:app", port=8080, log_level="info", reload=True)


if __name__ == "__main__":
    main()
