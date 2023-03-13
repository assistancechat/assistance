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

import collections
import torch
import asyncio
from asyncache import cached
from cachetools.keys import hashkey
from cachetools import LRUCache

from assistance._openai import get_embedding


async def get_top_questions_and_answers(openai_api_key, faq_data, queries, k=3):
    all_most_relevant_results = await _get_top_questions_and_answers(
        openai_api_key, faq_data, queries, k=k
    )

    collected_q_and_a_strings_with_score = collections.defaultdict(list)

    for most_relevant_results in all_most_relevant_results:
        for item in most_relevant_results:
            q_and_a_string = (
                f"Q: {item['question'].strip()}\nA: {item['answer'].strip()}"
            )

            collected_q_and_a_strings_with_score[q_and_a_string].append(item["score"])

    strings_and_scores = []
    for q_and_a_string, scores in collected_q_and_a_strings_with_score.items():
        sqrt_sum_of_square_scores = (sum(score**2 for score in scores)) ** 0.5
        strings_and_scores.append((q_and_a_string, sqrt_sum_of_square_scores))

    strings_and_scores.sort(key=lambda x: x[1], reverse=True)
    collected_q_and_a_strings = [x[0] for x in strings_and_scores]

    return collected_q_and_a_strings


async def _get_top_questions_and_answers(openai_api_key, faq_data, queries, k=3):
    queries = tuple(queries)
    queries_embedding = await _get_cuda_embeddings(
        queries, openai_api_key=openai_api_key
    )

    all_questions: tuple[str, ...] = tuple(
        [item["question"] for item in faq_data["items"]]
    )
    embeddings = await _get_cuda_embeddings(
        all_questions, openai_api_key=openai_api_key
    )
    all_queries_indices, all_queries_scores = top_k_embeddings(
        queries_embedding, embeddings, k
    )

    all_most_relevant_results = []

    for indices, scores in zip(all_queries_indices, all_queries_scores):
        most_relevant_results = [faq_data["items"][i] for i in indices]
        for item, score in zip(most_relevant_results, scores):
            item["score"] = score

        all_most_relevant_results.append(most_relevant_results)

    return all_most_relevant_results


def top_k_embeddings(queries, embeddings, k):
    k = torch.tensor(k, device="cuda")
    cosine_similarity, index = _top_k_embeddings(queries, embeddings, k)

    index = index.tolist()
    cosine_similarity = cosine_similarity.tolist()

    return index, cosine_similarity


@torch.jit.script  # type: ignore
def _top_k_embeddings(queries, embeddings, k):
    transpose_queries = queries.T
    embeddings_norm = torch.linalg.norm(embeddings, dim=1, keepdim=True)
    query_norm = torch.linalg.norm(transpose_queries, dim=0, keepdim=True)

    cosine_similarity = (
        (embeddings @ transpose_queries) / (embeddings_norm @ query_norm)
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
