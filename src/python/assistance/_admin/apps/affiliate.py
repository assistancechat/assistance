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

import streamlit as st
from jose import jwt

from assistance._admin import categories
from assistance._keys import get_jwt_key

ALGORITHM = "HS256"

JWT_SECRET_KEY = get_jwt_key()

CATEGORY = categories.ADMIN
TITLE = "Affiliate Links"


async def main():
    email = st.text_input(
        "Email address of the affiliate who is being associated with this link"
    )
    details = st.text_area(
        "Extra details to encode along with the affiliate link token (optional)"
    )

    affiliate_link_data = {
        "type": "affiliate",
        "email": email,
        "details": details,
    }

    if not st.button("Generate Affiliate Link"):
        st.stop()

    tag = _create_affiliate_tag(affiliate_link_data)
    st.write(f"https://globaltalent.work/?tag={tag}")

    payload = jwt.decode(tag, JWT_SECRET_KEY, algorithms=[ALGORITHM])

    st.write("## Affiliate token contents")
    st.write(payload)


def _create_affiliate_tag(data: dict):
    affiliate_tag = jwt.encode(data, JWT_SECRET_KEY, algorithm=ALGORITHM)

    return affiliate_tag
