# AIOS Event Bus + Durable State V0

Phase 9 introduces the event and state primitives needed for long-running AIOS executions.

## Event model

```text
Producer
   |
   v
 EventBus
   |
   +--> topic subscriber A
   +--> topic subscriber B
   +--> wildcard subscriber
```

Each event has a stable ID, topic, payload, timestamp, correlation ID, and optional causation ID. This gives later distributed implementations enough metadata for tracing event chains.

V0 is an in-process asynchronous bus. It is deliberately not presented as durable messaging yet.

## Execution state

```text
Execution
   |
   +--> status
   +--> step
   +--> checkpoint
   +--> version
   +--> updated_at
```

`StateStore` uses optimistic versioning. A writer can provide `expected_version`; a mismatch is rejected instead of silently overwriting newer state.

## Why this matters

An agent that runs for seconds can keep state in memory. An agent that runs for hours or days cannot depend on process memory.

The intended future flow is:

```text
Agent step
   |
   +--> persist checkpoint
   |
   +--> publish event
   |
   +--> continue

process crash
   |
   v
worker restarts
   |
   v
load checkpoint
   |
   v
resume
```

## Production evolution

The V0 contracts can later be backed by:

- SQLite for a single-machine deployment
- PostgreSQL for durable local/server state
- Redis or a message broker for transient distribution
- NATS/Kafka/etc. for higher-scale event streaming

Those technologies are implementation choices, not AIOS core contracts.

## Next work

Before 24/7 workers, AIOS should add cancellation, deadlines, persistent scheduler state, event replay/idempotency, and a worker lifecycle manager.
