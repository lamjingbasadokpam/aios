"""Provider-neutral agent memory store with an in-memory V0 backend."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from .contracts import MemoryQuery, MemoryRecord


class MemoryStore:
    """Durable-ready memory boundary; retrieval remains intentionally simple in V0."""

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

    def remember(self, content: str, *, namespace: str = "default", metadata: dict | None = None) -> MemoryRecord:
        """Create a memory record while keeping persistence implementation-neutral."""
        record = MemoryRecord(
            id=str(uuid4()),
            namespace=namespace,
            content=content,
            metadata=metadata or {},
            created_at=datetime.now(timezone.utc),
        )
        return self.add(record)

    def search_text(self, query: str, *, namespace: str = "default", limit: int = 5) -> list[MemoryRecord]:
        """Simple lexical retrieval used only as a V0 fallback before vector RAG."""
        if limit <= 0:
            return []
        terms = {term.lower() for term in query.split() if term.strip()}
        candidates = self.list(namespace)
        ranked = sorted(
            candidates,
            key=lambda record: sum(term in record.content.lower() for term in terms),
            reverse=True,
        )
        return [
            record for record in ranked
            if not terms or any(term in record.content.lower() for term in terms)
        ][:limit]
