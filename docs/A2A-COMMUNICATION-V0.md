# AIOS Agent-to-Agent Communication V0

Phase 18 introduces explicit communication between persistent agent identities.

```text
Agent A
   |
 A2AMessage
   |
 Message Bus
   |
 Agent B
```

## Message kinds

- `request` — ask another agent to perform work
- `response` — answer a request
- `event` — publish a fact without requiring a response
- `delegation` — transfer responsibility for a task

## Delivery lifecycle

```text
send
  |
  v
QUEUED
  |
receive
  v
DELIVERED
```

Unknown recipients fail immediately rather than silently dropping messages.

## Correlation

Requests can carry a `correlation_id`. Responses should reuse the request's correlation ID so an orchestrator can associate asynchronous replies with the originating operation.

## V0 limitation

The current bus is in-process and ephemeral. It is a reference implementation of the communication contract, not yet a durable distributed transport.

Future adapters should support:

- durable inbox/outbox
- retries and dead-letter queues
- idempotency keys
- authorization based on agent identity and policy
- cross-process delivery
- local-to-cloud communication
- message tracing

The agent identity remains the source of identity; workers/processes are only execution locations.
