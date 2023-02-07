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

import base64
import json

import streamlit as st
from cryptography.fernet import Fernet

from assistance._admin import categories
from assistance._keys import get_fernet_key

ALGORITHM = "HS256"

FERNET_SECRET_KEY = get_fernet_key()

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

    json_string = json.dumps(affiliate_link_data, indent=2)
    for_encryption = json_string.encode()

    fernet = Fernet(FERNET_SECRET_KEY)
    token = fernet.encrypt(for_encryption)
    tag = base64.urlsafe_b64encode(token).decode()

    st.write(f"https://globaltalent.work/?tag={tag}")

    decoded = base64.urlsafe_b64decode(tag.encode())
    decrypted = fernet.decrypt(decoded)

    loaded_token_data = json.loads(decrypted)

    st.write("## Token contents")
    st.write(loaded_token_data)
