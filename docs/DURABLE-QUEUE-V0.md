# AIOS Phase 13 — Durable Queue + Leases V0

Phase 13 changes task delivery from a best-effort in-memory queue into a lease-based execution contract.

```text
Scheduler
   |
   v
Durable Queue
   |
   | claim + lease
   v
Worker
   |
   +--> complete
   |
   +--> fail

worker dies
   |
   v
lease expires
   |
   v
queue recovers task
   |
   v
another worker claims it
```

## V0 guarantees

- Priority-aware claiming
- Worker-specific leases
- Lease expiry recovery
- Attempt counting
- Ownership checks for completion/failure
- Task state transitions

## Why leases matter

A worker must not permanently own a task merely because it claimed it. A lease gives the system a bounded ownership window.

```text
claim at 10:00
lease until 10:01

worker alive -> renew/complete
worker dead  -> lease expires -> task becomes claimable
```

## Important limitation

The implementation is still an in-memory reference backend. The *semantics* are durable-queue semantics, but the storage is not crash durable yet.

The next storage backend can implement the same operations in SQLite/PostgreSQL/Redis/etc.

## Production requirements

Before unattended 24/7 execution, add:

- atomic claim transactions
- lease renewal/heartbeat
- persistent storage
- idempotency keys
- dead-letter queues
- retry/backoff policy
- task cancellation
- queue metrics
- recovery/reconciliation worker

## Architecture after Phase 13

```text
                 Scheduler
                     |
                     v
              Durable Queue
                     |
              claim + lease
                     |
          +----------+----------+
          v          v          v
       Worker A   Worker B   Worker C
          |          |          |
          +----------+----------+
                     |
                 Orchestrator
                     |
            Event Bus / State
                     |
                 Supervisor
```
