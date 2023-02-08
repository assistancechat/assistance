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

from assistance._admin import categories
from assistance._affiliate import create_affiliate_tag, decrypt_affiliate_tag

CATEGORY = categories.ADMIN
TITLE = "Affiliate Links"


async def main():
    email = st.text_input(
        "Email address of the affiliate who is being associated with this link"
    )
    details = st.text_area(
        "Extra details to encode along with the affiliate link token (optional)"
    )

    domain = st.text_input("Domain to create the link for", "globaltalent.work")

    if not st.button("Generate Affiliate Link"):
        st.stop()

    tag = create_affiliate_tag(email, details)
    st.write(f"https://{domain}/?tag={tag}")

    loaded_token_data = decrypt_affiliate_tag(tag)

    st.write("## Token contents")
    st.write(loaded_token_data)
