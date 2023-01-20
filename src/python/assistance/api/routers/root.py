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


from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from assistance.api.login import (
    Token,
    User,
    create_temp_account,
    get_current_user,
    get_user_access_token,
)
from assistance.conversations import call_gpt_and_store_as_transcript
from assistance.store import store_file

router = APIRouter(
    prefix="",
    responses={404: {"description": "Not found"}},
)


@router.post("/login", response_model=Token)
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    access_token = get_user_access_token(form_data.username, form_data.password)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/temp-account")
async def temp_account():
    username = create_temp_account()

    return {"username": username}


class Prompt(BaseModel):
    record_grouping: str
    model_kwargs: dict
    prompt: str


@router.post("/prompt")
async def run_prompt(
    data: Prompt,
    current_user: User = Depends(get_current_user),
):
    response = await call_gpt_and_store_as_transcript(
        record_grouping=data.record_grouping,
        username=current_user.username,
        model_kwargs=data.model_kwargs,
        prompt=data.prompt,
    )

    return {"response": response}


class StoreDataRecordGroupingOptional(BaseModel):
    record_grouping: str | None = None
    content: str


@router.post("/save")
async def save_content(
    data: StoreDataRecordGroupingOptional,
    current_user: User = Depends(get_current_user),
):
    record_grouping = data.record_grouping

    if record_grouping is None:
        record_grouping = "career.assistance.chat"

    dirnames = [record_grouping, current_user.username, "save-api-call"]
    filename = "contents.txt"

    await store_file(dirnames=dirnames, filename=filename, contents=data.content)
