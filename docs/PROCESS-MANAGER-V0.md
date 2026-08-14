# AIOS Process Manager V0

Phase 22 establishes a portable process-lifecycle boundary for agents.

```text
Agent Identity
      |
Process Manager
      |
  +---+---+---+
  |   |   |   |
  A   B   C   D
  |   |   |   |
 PID endpoint state
```

## Lifecycle

`STARTING -> RUNNING -> STOPPING -> STOPPED` with `FAILED` representing an abnormal termination.

The manager records PID, IPC endpoint, restart count, and the last failure reason.

## Boundary

V0 deliberately does not embed Windows process creation or Named Pipe implementation into the core. Those belong to OS adapters. The process manager owns lifecycle state; an adapter owns actual process creation and termination.

## Windows direction

The first production adapter should use Windows-native process controls and Named Pipes. It should integrate with the Phase 16 sandbox/resource model and Phase 20 gateway so each agent process receives a constrained execution context and registered endpoint.

## Recovery direction

The supervisor should consume process failure events and decide whether to restart an agent. The process manager should remain a lifecycle mechanism, not become the policy engine.
