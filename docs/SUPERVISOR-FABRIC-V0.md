# AIOS Supervisor + Watchdog Fabric V0

Phase 11 adds a supervisor above Worker Fabric. Its job is health observation and bounded recovery, not task orchestration.

```text
                 Supervisor
                     |
              health / watchdog
                     |
       +-------------+-------------+
       v             v             v
    Worker A       Worker B      Worker C
       |             |             |
   heartbeat     heartbeat     heartbeat
```

## V0 capabilities

- Worker health reports
- Heartbeat timeout detection
- Failed-worker detection
- Configurable restart policy
- Maximum restart count
- Restart backoff
- Long-running watchdog loop
- Explicit supervisor shutdown

## Separation of concerns

```text
Orchestrator -> decides WHAT should run
Worker       -> performs the work
Supervisor   -> keeps workers healthy
StateStore   -> remembers execution state
EventBus     -> communicates changes
```

The supervisor should not silently invent tasks or modify agent plans.

## Important limitation

The watchdog currently supervises in-process `WorkerManager` workers. It is not yet an OS-level process supervisor. A worker process that takes down the Python runtime cannot be restarted by this component.

A later process supervisor will place this layer above independently managed worker processes.

## Target 24/7 architecture

```text
OS / Service Manager
        |
        v
AIOS Supervisor
        |
   +----+----+----------------+
   v         v                v
Local     Local             Cloud
Worker    Worker            Worker
   |         |                |
 Agent     Agent            Agent
   +---------+----------------+
             |
        Event Bus / State
```

Before production unattended operation, add persistent worker registry, process-level isolation, durable queues/leases, exponential backoff, idempotent recovery, and resource-aware health checks.
