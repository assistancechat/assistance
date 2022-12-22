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
from fastapi.security import OAuth2PasswordRequestForm

from .conversations import chat_response
from .keys import set_openai_api_key
from .login import Token, User, get_access_token, get_current_active_user

app = FastAPI()

set_openai_api_key()


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = get_access_token(form_data.username, form_data.password)

    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.post("/chat")
def chat(student_text: str, current_user: User = Depends(get_current_active_user)):
    response = chat_response(username=current_user.username, student_text=student_text)

    return {"response": response}


def main():
    uvicorn.run("assistance.api.main:app", port=8080, log_level="info", reload=True)


if __name__ == "__main__":
    main()
