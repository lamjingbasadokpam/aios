# AIOS Durable A2A Messaging V0

Phase 19 extends A2A from an in-process message bus toward reliable delivery semantics.

```text
Agent A
  |
Outbox / enqueue
  |
Durable message store
  |
Inbox for Agent B
  |
claim
  |
Agent B
```

## V0

- message records are retained separately from delivery state
- recipient inboxes are indexed by stable agent identity
- messages can be claimed
- delivery can be marked delivered or failed
- delivery attempts are tracked
- routing is idempotent for the same message ID

## Why this is separate from the A2A bus

The bus defines communication semantics. The durable store defines what survives between delivery attempts and process boundaries. A production backend can later implement the same store contract using SQLite/PostgreSQL or another durable queue.

## Reliability roadmap

V0 is a reference implementation and is still process-local. Production work must add transactional persistence, leases/visibility timeouts, retry policy, dead-letter queues, idempotency keys, authentication/authorization, and crash-safe acknowledgement.

The target architecture is:

```text
Local Agent                    Cloud Agent
     |                              |
   Outbox                         Outbox
     |                              |
     +-------- durable bus --------+
                    |
              delivery router
                    |
              Inbox / lease
```

This allows local and cloud agents to communicate without requiring either agent to know where the other is running.
