# AIOS Persistent Storage Fabric V0

Phase 14 separates durable storage contracts from their physical backend.

```text
AIOS components
     |
     v
StorageBackend contract
     |
  +--+----------------+
  |                   |
SQLite/Postgres     In-memory
production          reference
```

## V0 persisted domains

- execution checkpoints
- worker registry state
- append-only event records

The contract is asynchronous so a disk or network backend does not force API changes later.

## Design rule

Core AIOS components should depend on `StorageBackend`, never directly on PostgreSQL, Redis, SQLite, or a vendor SDK.

```text
Agent / Scheduler / Worker
             |
             v
       StorageBackend
             |
       concrete adapter
```

## Why the event journal matters

The event sequence provides a replay cursor. A future event-driven runtime can persist `last_processed_sequence` and resume consumption after restart without losing its place.

## Production backend roadmap

1. SQLite adapter for single-machine installations.
2. PostgreSQL adapter for durable multi-process installations.
3. Optional Redis adapter for low-latency coordination/leases.
4. Object storage for large artifacts, not primary transactional state.

The reference implementation intentionally remains in-memory in V0; adding a real database before the contracts stabilize would couple the kernel to an infrastructure choice too early.
