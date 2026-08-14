# AIOS Agent Context Integration V0

Phase 40 connects retrieval and context packing to the agent boundary.

```text
Agent state + query
        |
        v
HybridRetriever
        |
        v
ContextEngine
        |
        v
Bounded ContextPack
        |
        v
Model request
```

`AgentContextBuilder` is deliberately separate from `AgentLoop`: it prepares context, while the loop remains responsible for model/tool decisions.

## Rules

- Retrieval is scoped by namespace.
- Context budgets are enforced before model execution.
- Provenance is retained when memory becomes model context.
- The agent loop does not depend on a specific vector database or embedding provider.
- Context integration is read-only; memory writes remain an explicit operation.

Future phases can add conversation summarization, working-memory state, tool observations, system prompts, and provider-specific tokenizers without changing the retrieval contracts.
