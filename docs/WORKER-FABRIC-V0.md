# AIOS Worker Fabric V0

Worker Fabric turns AIOS execution into managed long-lived processes.

```text
WorkerManager
    |
    +--> Worker A --> Agent / task loop
    +--> Worker B --> Agent / task loop
    +--> Worker C --> Agent / task loop
```

## V0 capabilities

- Worker registration
- Bounded worker capacity
- Start/stop lifecycle
- Running/stopped/failed states
- Heartbeat timestamp
- Failure capture
- Global shutdown

## Worker identity

Every worker has a stable `worker_id`. The worker state is separate from the task or agent it runs. This distinction matters for future scheduling and distributed workers.

## What V0 does not yet provide

- automatic restart policy
- persistent worker registry
- OS process supervision
- distributed workers
- task queues
- lease/claim semantics
- heartbeat monitoring loop
- resource-aware placement
- remote/cloud workers

Those should be layered on top rather than hidden inside the worker contract.

## Target architecture

```text
                 Worker Manager
                       |
          +------------+------------+
          |            |            |
       Local-1      Local-2      Cloud-1
          |            |            |
        Agent        Agent        Agent
          |            |            |
          +------------+------------+
                       |
                   Event Bus
                       |
                  State Store
```

The same worker lifecycle contract should work for local and remote execution.
