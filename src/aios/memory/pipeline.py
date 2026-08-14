"""RAG context assembly over the Memory Fabric."""

from __future__ import annotations

from .contracts import MemoryQuery
from .retriever import MemoryRetriever


class RagPipeline:
    def __init__(self, retriever: MemoryRetriever) -> None:
        self.retriever = retriever

    def retrieve_context(self, query: str, namespace: str = "default", top_k: int = 5) -> str:
        hits = self.retriever.search(MemoryQuery(query=query, namespace=namespace, top_k=top_k))
        if not hits:
            return ""
        return "\n\n".join(
            f"[memory score={hit.score:.3f} source={hit.record.source}]\n{hit.record.content}"
            for hit in hits
        )

    def augment(self, query: str, namespace: str = "default", top_k: int = 5) -> str:
        context = self.retrieve_context(query, namespace, top_k)
        if not context:
            return query
        return f"Relevant memory:\n{context}\n\nUser/task query:\n{query}"
