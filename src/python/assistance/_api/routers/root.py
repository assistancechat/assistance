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

from assistance._api.utilities.login import (
    Token,
    create_temp_account,
    get_user_access_token,
)

router = APIRouter(prefix="")


@router.post("/login", response_model=Token)
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
