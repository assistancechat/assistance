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
from pydantic import BaseModel

from assistance.api.login import User, get_current_user
from assistance.summary.summary import summarise

router = APIRouter(prefix="/summarise")


class SummariseData(BaseModel):
    record_grouping: str
    query: str
    text: str


@router.post("/")
async def run_summarise(
    data: SummariseData,
    current_user: User = Depends(get_current_user),
):
    return await summarise(
        record_grouping=data.record_grouping,
        username=current_user.username,
        query=data.query,
        text=data.text,
    )
