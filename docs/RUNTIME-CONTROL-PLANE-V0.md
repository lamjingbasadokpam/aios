# AIOS Runtime Control Plane V0

Phase 49 introduces the control-plane boundary for managed agent runs.

```text
Control Plane
    |
    +--> inspect
    +--> pause
    +--> resume
    +--> cancel
    |
    v
RunHandle / RunState
    |
    v
Data Plane (agent/workflow execution)
```

## State machine

```text
CREATED -> RUNNING -> PAUSED -> RUNNING
    |                    |
    +--------------------+----> CANCELLED
    |
    +-------------------------> FAILED / COMPLETED (owned by execution runtime)
```

V0 provides an in-memory controller and deliberately does not attempt to forcibly interrupt arbitrary Python tasks. Cancellation is a control-plane intent; cooperative enforcement by executors is a later concern.

The controller grants no tool or model permissions. Authorization remains a separate policy boundary.
