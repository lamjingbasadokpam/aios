"""Integration between agent state, memory retrieval, and model context."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aios.memory.context import ContextEngine, ContextPack
from aios.memory.contracts import MemoryQuery
from aios.memory.gateway import MemoryAccessContext, MemoryGateway


@dataclass(frozen=True, slots=True)
class AgentContext:
    messages: tuple[dict[str, Any], ...]
    memory: ContextPack


class AgentContextBuilder:
    """Build bounded model context through the governed memory boundary."""

    def __init__(self, gateway: MemoryGateway, context_engine: ContextEngine) -> None:
        self.gateway = gateway
        self.context_engine = context_engine

    def build(
        self,
        *,
        query: str,
        messages: list[dict[str, Any]],
        access: MemoryAccessContext,
        namespace: str = "default",
        top_k: int = 8,
    ) -> AgentContext:
        hits = self.gateway.recall(
            MemoryQuery(query, namespace=namespace, top_k=top_k),
            context=access,
        )
        return AgentContext(tuple(messages), self.context_engine.pack(hits))

    def as_system_context(self, context: AgentContext) -> str:
        if not context.memory.items:
            return ""
        sections = [
            f"[Source: {item.source}]\n{item.content}" for item in context.memory.items
        ]
        return "Relevant memory:\n\n" + "\n\n".join(sections)
