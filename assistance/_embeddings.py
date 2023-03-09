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


import torch
import asyncio
from asyncache import cached
from cachetools.keys import hashkey
from cachetools import LRUCache

from assistance._openai import get_embedding


async def get_top_questions_and_answers(openai_api_key, faq_data, query, k=3):
    query_embedding = await _get_cuda_embedding(query, openai_api_key=openai_api_key)

    all_questions: tuple[str, ...] = tuple(
        [item["question"] for item in faq_data["items"]]
    )
    embeddings = await _get_cuda_embeddings(
        all_questions, openai_api_key=openai_api_key
    )
    indices, scores = top_k_embeddings(query_embedding, embeddings, k)

    most_relevant_results = [faq_data["items"][i] for i in indices]
    for item, score in zip(most_relevant_results, scores):
        item["relevance_score"] = score

    return [faq_data["items"][i] for i in indices]


def top_k_embeddings(query, embeddings, k):
    k = torch.tensor(k, device="cuda")
    cosine_similarity, index = _top_k_embeddings(query, embeddings, k)

    index = index.tolist()
    cosine_similarity = cosine_similarity.tolist()

    assert len(index) == 1
    assert len(cosine_similarity) == 1

    return index[0], cosine_similarity[0]


@torch.jit.script  # type: ignore
def _top_k_embeddings(query, embeddings, k):
    transpose_query = query.T
    embeddings_norm = torch.linalg.norm(embeddings, dim=1, keepdim=True)
    query_norm = torch.linalg.norm(transpose_query, dim=0, keepdim=True)

    cosine_similarity = (
        (embeddings @ transpose_query) / (embeddings_norm @ query_norm)
    ).T

    return torch.topk(cosine_similarity, k)


@cached(
    cache=LRUCache(maxsize=32),
    key=lambda questions, openai_api_key: hashkey(questions),
)
async def _get_cuda_embeddings(
    questions: tuple[str, ...], openai_api_key: str
) -> torch.Tensor:
    embeddings = await asyncio.gather(
        *[
            get_embedding(block=question, api_key=openai_api_key)
            for question in questions
        ]
    )
    return torch.tensor(embeddings, device="cuda")


@cached(
    cache=LRUCache(maxsize=32),
    key=lambda questions, openai_api_key: hashkey(questions),
)
async def _get_cuda_embedding(question: str, openai_api_key: str) -> torch.Tensor:
    embedding = await get_embedding(block=question, api_key=openai_api_key)
    return torch.tensor([embedding], device="cuda")
