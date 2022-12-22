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
from passlib.context import CryptContext
from pydantic import BaseModel

from .exceptions import CredentialsException
from .keys import get_jwt_key

SECRET_KEY = get_jwt_key()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException

        token_data = TokenData(username=username)
    except JWTError as e:
        raise CredentialsException from e

    user = _get_user(_fake_users_db, username=token_data.username)

    if user is None:
        raise CredentialsException

    return user


async def get_current_active_user(current_user: "User" = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


def get_access_token(username, password):
    user = _authenticate_user(_fake_users_db, username, password)

    if not user:
        raise CredentialsException

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
    username: str
    email: str | None = None
    preferred_name: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


_fake_users_db: dict[str, UserInDB] = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "preferred_name": "John",
        "full_name": "John Doe",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
}


def _verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def _get_password_hash(password):
    return pwd_context.hash(password)


def _get_user(db, username: str):
    if username not in db:
        return None

    user_dict = db[username]

    return UserInDB(**user_dict)


def _authenticate_user(fake_db, username: str, password: str):
    user = _get_user(fake_db, username)
    if not user:
        return False
    if not _verify_password(password, user.hashed_password):
        return False
    return user


def _create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
