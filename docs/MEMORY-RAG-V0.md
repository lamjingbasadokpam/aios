# AIOS Memory + RAG Fabric V0

## Purpose

Memory is a first-class AIOS service. Agents request context through a stable API rather than directly coupling themselves to a vector database or embedding provider.

```text
Agent
  |
  v
Memory / RAG API
  |
  +--> MemoryStore
  |
  +--> Retriever
  |
  +--> Context assembly
  |
  v
Model Router
```

## V0

The first backend is deliberately deterministic lexical retrieval. It provides the contracts and retrieval semantics without making a vector database or embedding model a kernel dependency.

Memory records have:

- content
- source
- namespace
- metadata
- creation time
- stable identifier

Queries support:

- namespace isolation
- metadata filters
- top-k retrieval

The RAG pipeline assembles retrieved records into a context block that can be supplied to the model runtime.

## Why lexical first

The goal of this phase is to prove the Memory API, isolation boundaries, and context assembly before introducing embedding infrastructure. A future retriever can implement the same contract using embeddings, BM25, a vector database, or a hybrid search strategy.

## Planned retrieval stack

```text
Query
  |
  +--> lexical retrieval
  +--> dense embedding retrieval
  +--> metadata filtering
  +--> reranking
  |
  v
Context assembler
  |
  v
Model
```

## Memory types

Future AIOS memory should distinguish:

- working memory — current execution context
- episodic memory — events and task outcomes
- semantic memory — durable facts/knowledge
- procedural memory — reusable workflows and skills
- external knowledge — indexed documents/data

V0 intentionally keeps one generic record contract. Specialization belongs above the storage boundary.

## Non-goals

- automatic embedding generation
- vector database dependency
- document ingestion workers
- chunking pipeline
- citation verification
- memory consolidation
- automatic long-term memory writes

These will be introduced incrementally.
