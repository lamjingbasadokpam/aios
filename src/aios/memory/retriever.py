"""Deterministic lexical retrieval backend for Memory V0."""

from __future__ import annotations

import re

from .contracts import MemoryHit, MemoryQuery
from .store import MemoryStore


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9_]+", text.lower()))


class MemoryRetriever:
    def __init__(self, store: MemoryStore) -> None:
        self.store = store

    def search(self, query: MemoryQuery) -> list[MemoryHit]:
        q = _tokens(query.query)
        hits: list[MemoryHit] = []
        for record in self.store.query_candidates(query):
            words = _tokens(record.content)
            if not q:
                score = 0.0
            else:
                score = len(q & words) / len(q)
            if score > 0:
                hits.append(MemoryHit(record=record, score=score))
        hits.sort(key=lambda hit: (-hit.score, hit.record.created_at))
        return hits[: max(0, query.top_k)]
