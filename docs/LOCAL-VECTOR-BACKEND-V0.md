# AIOS Local Vector Backend V0

Phase 36 supplies a dependency-light local implementation of the retrieval contracts.

```text
Text
 |
HashEmbedder
 |
Vector
 |
InMemoryVectorIndex
 |
Cosine similarity
 |
Top-K MemoryHit
```

## Scope

`HashEmbedder` is a deterministic infrastructure backend for local development and contract testing. It is deliberately not presented as a production semantic embedding model.

`InMemoryVectorIndex` provides namespace-scoped cosine similarity and replacement/upsert by memory ID.

## Why start here

This gives AIOS a complete local vector path without forcing a heavyweight database or model dependency into the core. Real embedding models and persistent vector databases can later implement the same `Embedder` and `VectorIndex` contracts.

## Production path

A future deployment can replace either component independently:

```text
AIOS RetrievalEngine
      |
      +--> real local embedding model
      |
      +--> Qdrant / pgvector / FAISS / LanceDB adapter
```

The agent and worker layers remain unchanged.
