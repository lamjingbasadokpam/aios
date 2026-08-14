# AIOS Model Fabric V0

## Implemented

Phase 2 introduces the first provider-independent inference boundary.

```text
Agent / Runtime
      |
      v
 ModelRouter
      |
      v
 ModelRegistry
      |
      +---- ModelProvider
              |
              +---- Local adapter
              +---- Cloud adapter (future)
```

## V0 contracts

- `Model`: capability and resource metadata
- `ModelCapabilities`: supported inference features
- `InferenceRequest`: normalized request
- `InferenceResponse`: normalized response
- `ModelProvider`: provider adapter protocol
- `ModelRegistry`: provider/model discovery
- `ModelRouter`: capability and locality selection

## Why the router exists

Agents must not contain logic such as `if ollama then ...` or `if openai then ...`. They ask AIOS for a model capability. The router selects an appropriate provider/model.

## Local-first rule

V0 supports locality-aware routing. A caller can request `local`, preventing the router from selecting a cloud provider.

## Mock provider

A deterministic `mock-local` adapter exists only to prove the contracts without requiring a model server or GPU. It is not the production inference backend.

## Next model adapter

The next implementation should add a real local provider, most likely through an adapter around a local inference server/runtime. The adapter should implement `ModelProvider` and require no changes to Kernel contracts or Agent Runtime contracts.

## Explicit non-goals

V0 does not yet implement:

- automatic model downloading
- GPU scheduling
- token accounting
- model fine-tuning
- prompt caching
- RAG
- agent reasoning
- tool calling execution
- cloud failover

Those belong to later layers.
