# AIOS Scheduler + Task Queue V0

Phase 12 adds delayed, recurring, priority-aware task scheduling.

```text
                 Scheduler
                     |
                     v
                TaskQueue
                     |
          +----------+----------+
          |          |          |
       priority    run_at    recurring
          |          |          |
          +----------+----------+
                     |
                     v
                 Worker Pool
```

## V0 capabilities

- Immediate/due tasks
- Delayed tasks through `run_at`
- Priority ordering
- Bounded concurrent execution
- Recurring tasks
- Maximum recurring run count
- Scheduler start/stop

## Scheduling is separate from orchestration

Orchestration answers:

> What depends on what?

Scheduling answers:

> When should this work become runnable?

Workers answer:

> Where/how should runnable work execute?

Supervisor answers:

> Is the worker healthy?

Keeping these responsibilities separate lets AIOS later replace the local queue with a durable distributed queue without changing agent logic.

## Current limitation

V0 keeps the queue in memory. Restarting the AIOS process loses scheduled items. Production 24/7 operation requires a durable queue and persistent schedule registry.

## Target flow

```text
Schedule
   |
   v
Durable Task Queue
   |
   v
Claim / Lease
   |
   v
Worker
   |
   +--> Agent
   +--> Tool
   +--> Model
   |
   v
Checkpoint + Event
```

That durable claim/lease layer is the next important infrastructure step before distributed or cloud workers.
