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


from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from .exceptions import CredentialsException
from .keys import get_jwt_key
from .paths import USERS

SECRET_KEY = get_jwt_key()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException

        token_data = TokenData(username=username)

    except JWTError as e:
        raise CredentialsException from e

    user = _get_user(username=token_data.username)

    return user


async def get_current_active_user(current_user: "User" = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


def get_access_token(username, password):
    user = _authenticate_user(username, password)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = _create_access_token(
        data={"sub": f"username:{user.username}"}, expires_delta=access_token_expires
    )

    return access_token


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    # username is the user's email
    username: str


class UserInDB(User):
    generated_password: str


def _get_user(username: str):
    path = USERS / username

    try:
        with open(path, encoding="utf8") as f:
            stored_password = f.read().strip()
    except FileNotFoundError as e:
        raise CredentialsException from e

    return UserInDB(username=username, generated_password=stored_password)


# We are generating random cryptographic tokens and assigning them as
# passwords for the user. User's aren't making their own passwords. We
# are sending them a signin link.
def _authenticate_user(username: str, password: str):
    user = _get_user(username)

    if not user or password != user.generated_password:
        raise CredentialsException

    return user


def _create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
