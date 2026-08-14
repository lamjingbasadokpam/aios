"""Document ingestion and deterministic chunking for AIOS RAG."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol
from uuid import uuid4

from .contracts import MemoryRecord


@dataclass(frozen=True, slots=True)
class Document:
    content: str
    source: str
    document_id: str
    metadata: dict[str, Any]


class DocumentLoader(Protocol):
    def load(self, source: str) -> Document: ...


@dataclass(frozen=True, slots=True)
class Chunk:
    content: str
    chunk_id: str
    document_id: str
    source: str
    index: int
    metadata: dict[str, Any]


class TextChunker:
    def __init__(self, max_chars: int = 1200, overlap: int = 150) -> None:
        if max_chars <= 0 or overlap < 0 or overlap >= max_chars:
            raise ValueError("overlap must be >= 0 and smaller than max_chars")
        self.max_chars = max_chars
        self.overlap = overlap

    def chunk(self, document: Document) -> list[Chunk]:
        text = document.content.strip()
        if not text:
            return []
        chunks: list[Chunk] = []
        start = 0
        index = 0
        while start < len(text):
            end = min(start + self.max_chars, len(text))
            if end < len(text):
                boundary = max(text.rfind("\n", start, end), text.rfind(" ", start, end))
                if boundary > start:
                    end = boundary
            content = text[start:end].strip()
            if content:
                chunks.append(Chunk(content, str(uuid4()), document.document_id, document.source, index, dict(document.metadata)))
                index += 1
            next_start = end - self.overlap
            start = next_start if next_start > start else end
        return chunks


def chunks_to_records(chunks: list[Chunk], namespace: str = "default") -> list[MemoryRecord]:
    return [
        MemoryRecord(
            content=chunk.content,
            source=chunk.source,
            memory_id=chunk.chunk_id,
            namespace=namespace,
            metadata={**chunk.metadata, "document_id": chunk.document_id, "chunk_index": chunk.index},
        )
        for chunk in chunks
    ]
