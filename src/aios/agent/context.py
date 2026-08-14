"""Integration between agent state, memory retrieval, and model context."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from aios.memory.context import ContextEngine, ContextPack
from aios.memory.contracts import MemoryQuery
from aios.memory.hybrid import HybridRetriever


@dataclass(frozen=True, slots=True)
class AgentContext:
    messages: tuple[dict[str, Any], ...]
    memory: ContextPack


class AgentContextBuilder:
    """Builds bounded model context from conversation state and retrieved memory."""

    def __init__(self, retriever: HybridRetriever, context_engine: ContextEngine) -> None:
        self.retriever = retriever
        self.context_engine = context_engine

    async def build(
        self,
        *,
        query: str,
        messages: list[dict[str, Any]],
        namespace: str = "default",
        top_k: int = 8,
    ) -> AgentContext:
        result = await self.retriever.retrieve(MemoryQuery(query, namespace=namespace, top_k=top_k))
        return AgentContext(tuple(messages), self.context_engine.pack(list(result.hits)))

    def as_system_context(self, context: AgentContext) -> str:
        if not context.memory.items:
            return ""
        sections = [
            f"[Source: {item.source}]\n{item.content}" for item in context.memory.items
        ]
        return "Relevant memory:\n\n" + "\n\n".join(sections)
