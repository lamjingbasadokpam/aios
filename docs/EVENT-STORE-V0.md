# AIOS Event Store V0

Phase 46 adds an append-only persistence boundary for runtime events.

```text
RuntimeEvent
    |
    v
 EventBus
    |
    +-------> live subscribers
    |
    v
 EventStore
    |
    +--> append
    +--> query by correlation ID / type
    +--> replay
```

## Scope

`EventStore` is provider-neutral. `InMemoryEventStore` is the deterministic V0 implementation used for local operation and contract testing.

Events remain immutable. The store appends events in publication order and can replay a filtered sequence to a handler.

## Correlation

`correlation_id` is the primary V0 trace key. A workflow, agent run, or future distributed execution can assign one ID and later reconstruct its event stream.

## Durability boundary

V0 intentionally does not pretend that in-memory storage survives process crashes. A future durable adapter can target SQLite, PostgreSQL, an event log, or another persistence system without changing the event contract.

## Replay safety

Replay invokes a consumer again; it does not claim that handlers are idempotent. Consumers that cause external side effects must provide their own idempotency guarantees before replay is used operationally.
