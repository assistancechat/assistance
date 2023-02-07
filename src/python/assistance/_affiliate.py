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

from cryptography.fernet import Fernet

from assistance._keys import get_fernet_key

FERNET_SECRET_KEY = get_fernet_key()


def create_affiliate_tag(email: str, details: str):
    affiliate_tag_data = {
        "type": "affiliate",
        "email": email,
        "details": details,
    }

    json_string = json.dumps(affiliate_tag_data, indent=2)
    for_encryption = json_string.encode()

    fernet = Fernet(FERNET_SECRET_KEY)
    encrypted = fernet.encrypt(for_encryption)
    tag = base64.urlsafe_b64encode(encrypted).decode()

    return tag


def decrypt_affiliate_tag(tag: str):
    decoded = base64.urlsafe_b64decode(tag.encode())

    fernet = Fernet(FERNET_SECRET_KEY)
    decrypted = fernet.decrypt(decoded)

    loaded_token_data = json.loads(decrypted)

    return loaded_token_data
