# AIOS Agent Memory V0

Phase 34 establishes the memory boundary between an agent and persistent knowledge.

```text
Agent
  |
  v
Memory Store
  |
  +-- namespace
  +-- source
  +-- metadata
  +-- content
  |
  +--> lexical V0 retrieval
  |
  +--> future vector / hybrid RAG
```

## Memory vs RAG

Memory is the system of record for information an agent is allowed to retain. RAG is a retrieval strategy over that information. They are deliberately separate contracts.

## V0

The in-memory store supports explicit writes, namespace isolation, metadata filtering through `MemoryQuery`, and simple lexical retrieval. It is a deterministic fallback, not the final semantic retrieval engine.

## Security boundary

Namespaces are part of the memory contract. A future persistent backend must preserve namespace and authorization boundaries rather than treating the vector database as an unrestricted global store.

## Next

Phase 35 can add an embedding/retrieval abstraction without forcing a specific vector database into the core runtime.
