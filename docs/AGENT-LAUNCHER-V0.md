# AIOS Agent Launcher V0

Phase 29 connects the declarative agent record to an OS process launcher.

```text
Manifest
  |
  v
Agent Record
  |
  v
Agent Launcher
  |       \
  |        +-- execution environment
  |        +-- working directory
  |        +-- launch command
  v
OS Process Adapter
  |
  v
Worker Process
  |
  v
Lifecycle Controller
```

## Responsibilities

The launcher builds a validated launch request from the agent record, delegates actual process creation to an OS adapter, then reports the resulting PID and endpoint to the lifecycle controller.

The launcher does not itself implement sandboxing, resource enforcement, IPC protocol, or model execution.

## Why this boundary matters

A Windows process adapter, Linux process adapter, container launcher, or cloud worker launcher can implement the same `ProcessLauncher` contract. The agent lifecycle and registry layers remain unchanged.

## V0 limitation

The command is still supplied by the caller. A future agent runtime/worker specification will resolve the worker entrypoint from the profile and runtime backend. Resource and sandbox enforcement must also be wired into the OS adapter before this is considered a hardened production launcher.
