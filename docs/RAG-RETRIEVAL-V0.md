# AIOS Retrieval / RAG V0

Phase 35 separates retrieval strategy from memory storage and vector infrastructure.

```text
Query
  |
  v
RetrievalEngine
  |
  +--> lexical fallback --> MemoryStore
  |
  +--> embedding --> VectorIndex
```

## Contracts

- `Embedder`: converts text into vectors.
- `VectorIndex`: stores vectors and performs similarity search.
- `RetrievalEngine`: chooses the configured vector path or deterministic lexical fallback.
- `RetrievalResult`: returns hits plus the strategy used.

## Design rules

- No vector database is hard-coded into AIOS.
- No embedding provider is hard-coded into AIOS.
- Memory storage and retrieval are separate boundaries.
- The lexical path is a fallback, not a substitute for semantic RAG.
- A vector backend must preserve namespace isolation.

## Next evolution

Future phases can add chunking, embedding caches, hybrid lexical+vector ranking, reranking, freshness/recency scoring, provenance, and context packing without changing the agent worker contract.
