"""Local dependency-light vector embedding/index backend for AIOS V0."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Sequence

from .contracts import MemoryHit, MemoryRecord


class HashEmbedder:
    """Deterministic local embedding based on hashed tokens.

    This is an infrastructure/testing backend, not a semantic model. It keeps
    AIOS fully local and dependency-light until a real embedding provider is configured.
    """

    def __init__(self, dimensions: int = 256) -> None:
        if dimensions <= 0:
            raise ValueError("dimensions must be positive")
        self.dimensions = dimensions

    async def embed(self, texts: Sequence[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def _embed(self, text: str) -> list[float]:
        vector = [0.0] * self.dimensions
        for token in re.findall(r"\w+", text.lower()):
            index = hash(token) % self.dimensions
            vector[index] += 1.0
        norm = math.sqrt(sum(value * value for value in vector))
        return [value / norm for value in vector] if norm else vector


@dataclass(slots=True)
class _VectorRecord:
    record: MemoryRecord
    vector: list[float]


class InMemoryVectorIndex:
    """Simple cosine-similarity index for local V0 operation."""

    def __init__(self) -> None:
        self._records: list[_VectorRecord] = []

    async def upsert(self, records: Sequence[MemoryRecord], vectors: Sequence[Sequence[float]]) -> None:
        if len(records) != len(vectors):
            raise ValueError("records and vectors must have equal length")
        for record, vector in zip(records, vectors):
            self._records = [item for item in self._records if item.record.memory_id != record.memory_id]
            self._records.append(_VectorRecord(record, list(vector)))

    async def search(self, vector: Sequence[float], *, namespace: str, top_k: int) -> list[MemoryHit]:
        if top_k <= 0:
            return []
        scored: list[MemoryHit] = []
        for item in self._records:
            if item.record.namespace != namespace or len(item.vector) != len(vector):
                continue
            score = sum(a * b for a, b in zip(item.vector, vector))
            scored.append(MemoryHit(item.record, score))
        scored.sort(key=lambda hit: hit.score, reverse=True)
        return scored[:top_k]
