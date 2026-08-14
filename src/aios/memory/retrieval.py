"""Provider-neutral embedding and retrieval contracts for AIOS RAG."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

from .contracts import MemoryHit, MemoryQuery, MemoryRecord
from .store import MemoryStore


class Embedder(Protocol):
    async def embed(self, texts: Sequence[str]) -> list[list[float]]: ...


class VectorIndex(Protocol):
    async def upsert(self, records: Sequence[MemoryRecord], vectors: Sequence[Sequence[float]]) -> None: ...
    async def search(self, vector: Sequence[float], *, namespace: str, top_k: int) -> list[MemoryHit]: ...


@dataclass(frozen=True, slots=True)
class RetrievalResult:
    hits: tuple[MemoryHit, ...]
    strategy: str


class RetrievalEngine:
    """Hybrid-ready retrieval boundary with lexical V0 fallback."""

    def __init__(self, store: MemoryStore, embedder: Embedder | None = None, index: VectorIndex | None = None) -> None:
        self.store = store
        self.embedder = embedder
        self.index = index

    async def index_records(self, records: Sequence[MemoryRecord]) -> None:
        if not records:
            return
        if self.embedder is None or self.index is None:
            raise RuntimeError("vector retrieval is not configured")
        vectors = await self.embedder.embed([record.content for record in records])
        if len(vectors) != len(records):
            raise ValueError("embedder returned a vector count mismatch")
        await self.index.upsert(records, vectors)

    async def retrieve(self, query: MemoryQuery) -> RetrievalResult:
        if query.top_k <= 0:
            return RetrievalResult((), "none")
        if self.embedder is not None and self.index is not None:
            vectors = await self.embedder.embed([query.query])
            if len(vectors) != 1:
                raise ValueError("embedder must return one vector for a query")
            hits = await self.index.search(vectors[0], namespace=query.namespace, top_k=query.top_k)
            return RetrievalResult(tuple(hits), "vector")
        records = self.store.search_text(query.query, namespace=query.namespace, limit=query.top_k)
        return RetrievalResult(tuple(MemoryHit(record, 1.0) for record in records), "lexical")
