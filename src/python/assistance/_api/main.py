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
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from assistance import _ctx, _logging
from assistance._config import ROOT_DOMAIN

from .routers import chat, email, forms, stripe

_logging.main()


app = FastAPI()

origins = [
    f"https://enquire.{ROOT_DOMAIN}",
    f"https://student.{ROOT_DOMAIN}",
    "https://globaltalent.work",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(stripe.router)
app.include_router(forms.router)
app.include_router(email.router)


@app.on_event("startup")
async def startup_event():
    _ctx.open_session()


@app.on_event("shutdown")
async def shutdown_event():
    await _ctx.close_session()


def main():
    uvicorn.run("assistance._api.main:app", port=8000, log_level="info", reload=True)


if __name__ == "__main__":
    main()
