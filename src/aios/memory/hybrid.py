"""Hybrid lexical/vector retrieval and deterministic reranking."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .contracts import MemoryHit, MemoryQuery
from .retrieval import RetrievalEngine


@dataclass(frozen=True, slots=True)
class HybridResult:
    hits: tuple[MemoryHit, ...]
    strategy: str


class HybridRetriever:
    """Combines lexical and vector candidates with reciprocal-rank fusion."""

    def __init__(self, engine: RetrievalEngine) -> None:
        self.engine = engine

    async def retrieve(self, query: MemoryQuery, *, candidate_k: int = 20) -> HybridResult:
        if query.top_k <= 0:
            return HybridResult((), "none")
        candidate_k = max(candidate_k, query.top_k)
        lexical_records = self.engine.store.search_text(
            query.query, namespace=query.namespace, limit=candidate_k
        )
        lexical = [MemoryHit(record, 1.0) for record in lexical_records]
        vector = []
        if self.engine.embedder is not None and self.engine.index is not None:
            vectors = await self.engine.embedder.embed([query.query])
            if len(vectors) != 1:
                raise ValueError("embedder must return one vector for a query")
            vector = await self.engine.index.search(
                vectors[0], namespace=query.namespace, top_k=candidate_k
            )
        else:
            return HybridResult(tuple(lexical[: query.top_k]), "lexical")

        fused: dict[Any, tuple[MemoryHit, float]] = {}
        k = 60.0
        for rank, hit in enumerate(lexical, 1):
            fused[hit.record.memory_id] = (hit, 1.0 / (k + rank))
        for rank, hit in enumerate(vector, 1):
            current = fused.get(hit.record.memory_id)
            contribution = 1.0 / (k + rank)
            fused[hit.record.memory_id] = (
                hit if current is None else current[0],
                contribution if current is None else current[1] + contribution,
            )
        ranked = sorted(fused.values(), key=lambda item: item[1], reverse=True)
        return HybridResult(tuple(item[0] for item in ranked[: query.top_k]), "hybrid_rrf")
