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


from assistance.search.search import alphacrucis_search
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .login.utilities import User, get_current_user

router = APIRouter(
    prefix="/search",
    responses={404: {"description": "Not found"}},
)


class SearchData(BaseModel):
    record_grouping: str
    query: str


@router.post("/search/alphacrucis")
async def run_alphacrucis_search(
    data: SearchData,
    _current_user: User = Depends(get_current_user),
):
    result = await alphacrucis_search(query=data.query)

    return result
