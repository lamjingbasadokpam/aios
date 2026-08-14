# AIOS Agent Execution Profile V0

Phase 25 unifies the execution-facing configuration of an agent into one declarative contract.

```text
Agent Profile
   |
   +-- identity/model
   +-- tools
   +-- sandbox
   +-- resource limits
   +-- network policy
   +-- transport
   +-- environment
          |
          v
    Process Manager
          |
    Windows Runtime
          |
   Job Object + IPC
          |
       Worker
```

## Design rule

The profile describes desired capabilities and constraints. It does not itself spawn processes, enforce security, or select a cloud provider. Those responsibilities remain with the runtime, sandbox, resource controller, and gateway layers.

## V0 fields

- stable agent ID
- model identifier
- sandbox profile
- memory/CPU/process limits
- network allowance
- allowed tools
- transport
- environment variables
- extensible metadata

## Why this matters

A single profile can describe the same logical agent whether it runs in-process, as a local Windows worker, or eventually in a remote/cloud worker. The execution backend changes; the agent contract does not.
