# AIOS Memory Fabric

**Version:** 1.0
**Status:** Frozen

## Purpose

Memory Fabric provides durable and temporary knowledge to agents while preserving provenance, trust, retrieval semantics, and lifecycle policy.

## Memory classes

### Working memory

Short-lived context required for an active task.

### Episodic memory

Records of prior agent/task experiences, decisions, outcomes, and observations.

### Semantic memory

Generalized facts and concepts accumulated from trusted sources and prior work.

### Procedural memory

Reusable procedures, workflows, skills, and operating patterns.

### Knowledge

External or user-provided documents and information indexed for retrieval.

## Retrieval

Retrieval may combine:

```text
Query
 -> lexical search
 -> vector search
 -> metadata filters
 -> graph/relationship lookup
 -> temporal filters
 -> ranking
 -> provenance/trust filtering
 -> context assembly
```

No single retrieval technique is mandatory.

## RAG

RAG is a capability implemented by Memory Fabric. It is not synonymous with the memory architecture.

## Provenance

Memory records should identify, where possible:

- source
- ingestion time
- creator/agent
- model or tool involved
- trust classification
- transformations
- related task

## Memory lifecycle

Memory should support creation, retrieval, update, invalidation, retention, consolidation, and deletion according to policy.

## Context discipline

Only relevant memory should enter model context. Retrieval results should be bounded, ranked, deduplicated, and labeled with provenance.

## Storage boundary

Memory interfaces remain independent of specific storage engines. A future implementation may combine relational, document, vector, full-text, and graph storage without changing the Agent Runtime contract.
