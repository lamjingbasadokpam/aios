"""RAG context assembly over the Memory Fabric."""

from __future__ import annotations

from .contracts import MemoryQuery
from .gateway import MemoryAccessContext, MemoryGateway


class RagPipeline:
    def __init__(self, gateway: MemoryGateway) -> None:
        self.gateway = gateway

    def retrieve_context(
        self,
        query: str,
        context: MemoryAccessContext,
        namespace: str = "default",
        top_k: int = 5,
    ) -> str:
        hits = self.gateway.recall(
            MemoryQuery(
                query=query,
                namespace=namespace,
                top_k=top_k,
            ),
            context=context,
        )

        if not hits:
            return ""

        return "\n\n".join(
            f"[memory score={hit.score:.3f} source={hit.record.source}]\n"
            f"{hit.record.content}"
            for hit in hits
        )

    def augment(
        self,
        query: str,
        context: MemoryAccessContext,
        namespace: str = "default",
        top_k: int = 5,
    ) -> str:
        memory_context = self.retrieve_context(
            query,
            context,
            namespace,
            top_k,
        )

        if not memory_context:
            return query

        return (
            f"Relevant memory:\n{memory_context}\n\n"
            f"User/task query:\n{query}"
        )