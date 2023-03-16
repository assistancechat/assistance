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

import asyncio
import collections

import aiofiles
import torch
from asyncache import cached
from cachetools import LRUCache
from cachetools.keys import hashkey

from assistance._openai import get_embedding
from assistance._paths import AI_REGISTRY_DIR


async def get_closest_functions(openai_api_key, docstring, k=3):
    docstring_embedding = await _get_cuda_embeddings(
        blocks=(docstring,), openai_api_key=openai_api_key
    )

    docstring_hashes, all_docstrings = await _get_all_docstrings()

    if len(all_docstrings) <= k:
        return docstring_hashes, all_docstrings

    registry_embeddings = await _get_cuda_embeddings(
        all_docstrings, openai_api_key=openai_api_key
    )

    indices, _scores = top_k_embeddings(docstring_embedding, registry_embeddings, k)

    top_docstring_hashes: list[str] = []
    top_docstrings: list[str] = []

    for index in indices:
        top_docstring_hashes.append(docstring_hashes[index])
        top_docstrings.append(all_docstrings[index])

    return top_docstring_hashes, top_docstrings


# TODO: Have a fancy way to cache this, and then have a file lister that
# clobbers the cache when a file is added.
async def _get_all_docstrings():
    docstring_hashes: list[str] = []
    coroutines = []
    for path in list(AI_REGISTRY_DIR.joinpath("docstrings").glob("*")):
        coroutines.append(_get_file_contents(path))
        docstring_hashes.append(path.stem)

    all_docstrings: tuple[str, ...] = tuple(await asyncio.gather(*coroutines))

    return docstring_hashes, all_docstrings


async def _get_file_contents(path):
    async with aiofiles.open(path, "r") as f:
        return await f.read()


async def get_top_questions_and_answers(openai_api_key, faq_data, queries, k=3):
    all_most_relevant_results = await _get_top_questions_and_answers(
        openai_api_key, faq_data, queries, k=k
    )

    collected_q_and_a_strings_with_score = collections.defaultdict(list)

    for most_relevant_results in all_most_relevant_results:
        for item in most_relevant_results:
            q_and_a_string = f"Question: {item['question'].strip()}\nAnswer: {item['answer'].strip()}"

            collected_q_and_a_strings_with_score[q_and_a_string].append(item["score"])

    strings_and_scores = []
    for q_and_a_string, scores in collected_q_and_a_strings_with_score.items():
        sqrt_sum_of_square_scores = (sum(score**2 for score in scores)) ** 0.5
        strings_and_scores.append((q_and_a_string, sqrt_sum_of_square_scores))

    strings_and_scores.sort(key=lambda x: x[1], reverse=True)

    responses_with_score = []
    for string, score in strings_and_scores:
        responses_with_score.append(f"Importance Score: {score:.2f}\n{string}")

    return responses_with_score


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
    blocks: tuple[str, ...], openai_api_key: str
) -> torch.Tensor:
    embeddings = await asyncio.gather(
        *[get_embedding(block=block, api_key=openai_api_key) for block in blocks]
    )
    return torch.tensor(embeddings, device="cuda")
