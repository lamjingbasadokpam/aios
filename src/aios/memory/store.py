"""Minimal durable-ready memory store interface with an in-memory V0 backend."""

from __future__ import annotations

from .contracts import MemoryQuery, MemoryRecord


class MemoryStore:
    def __init__(self) -> None:
        self._records: list[MemoryRecord] = []

    def add(self, record: MemoryRecord) -> MemoryRecord:
        self._records.append(record)
        return record

    def list(self, namespace: str = "default") -> list[MemoryRecord]:
        return [r for r in self._records if r.namespace == namespace]

    def query_candidates(self, query: MemoryQuery) -> list[MemoryRecord]:
        records = self.list(query.namespace)
        if not query.metadata_filter:
            return records
        return [
            r for r in records
            if all(r.metadata.get(k) == value for k, value in query.metadata_filter.items())
        ]
