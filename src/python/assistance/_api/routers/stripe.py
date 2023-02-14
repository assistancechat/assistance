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

import logging

import stripe
import stripe.error
from fastapi import APIRouter, Header, Request

from assistance._keys import get_stripe_webhook_key

router = APIRouter(prefix="/stripe")

ENDPOINT_SECRET = get_stripe_webhook_key()


# Inspired by https://github.com/ianrufus/youtube/blob/783ec64bf86cc79ee36759a075d5f939983bb7e5/fastapi-stripe-webhook/app.py#L67-L91
@router.post("")
async def handle_stripe(request: Request, stripe_signature: str = Header(None)):
    data = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload=data, sig_header=stripe_signature, secret=ENDPOINT_SECRET
        )
    except ValueError as e:
        raise e
    except stripe.error.SignatureVerificationError as e:
        raise e

    logging.info(event)
