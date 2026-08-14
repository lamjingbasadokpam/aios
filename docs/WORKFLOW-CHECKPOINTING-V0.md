# AIOS Workflow Checkpointing V0

Phase 44 introduces a persistence boundary for workflow state.

```text
WorkflowState
    |
    v
CheckpointStore
    |
    +--> save
    |
    +--> load
    |
    v
restore after process restart
```

## Scope

`CheckpointStore` is provider-neutral. `InMemoryCheckpointStore` is the V0 implementation for deterministic local operation and contract testing.

The checkpoint captures workflow lifecycle status, completed/failed step IDs, and step results.

## Design rules

- Persistence is separate from workflow execution.
- The workflow layer does not depend on a database implementation.
- Missing checkpoints are a normal `None` result.
- Serialized state is restored into typed workflow state.
- A future durable adapter can use SQLite, PostgreSQL, Redis, or another store without changing workflow contracts.

V0 does not claim crash-safe exactly-once execution. Durable checkpoints plus step-level idempotency are required before distributed execution can make that guarantee.
