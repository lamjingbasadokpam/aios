"""Context budgeting and packing for AIOS agents."""

from __future__ import annotations

from dataclasses import dataclass

from .contracts import MemoryHit


@dataclass(frozen=True, slots=True)
class ContextItem:
    content: str
    score: float
    source: str
    metadata: dict


@dataclass(frozen=True, slots=True)
class ContextPack:
    items: tuple[ContextItem, ...]
    estimated_tokens: int
    truncated: bool


class ContextEngine:
    """Deterministically deduplicates, ranks and packs retrieved memory."""

    def __init__(self, max_tokens: int = 2048) -> None:
        if max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        self.max_tokens = max_tokens

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        return max(1, (len(text) + 3) // 4)

    def pack(self, hits: list[MemoryHit]) -> ContextPack:
        seen: set[str] = set()
        items: list[ContextItem] = []
        used = 0
        truncated = False
        for hit in sorted(hits, key=lambda value: value.score, reverse=True):
            content = hit.record.content.strip()
            key = content.casefold()
            if not content or key in seen:
                continue
            cost = self._estimate_tokens(content)
            if used + cost > self.max_tokens:
                truncated = True
                continue
            seen.add(key)
            items.append(ContextItem(content, hit.score, hit.record.source, dict(hit.record.metadata)))
            used += cost
        return ContextPack(tuple(items), used, truncated)
