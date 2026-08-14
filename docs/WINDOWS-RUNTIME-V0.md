# AIOS Windows Native Runtime V0

Phase 23 completes the Windows-specific execution boundary without leaking Windows APIs into the AIOS core.

```text
Agent Identity
      |
Process Manager
      |
Windows Runtime Adapter
      +-------------------+
      |                   |
Process Adapter      Named Pipe Adapter
      |                   |
Windows process      \\.\pipe\...
      |                   |
      +---------+---------+
                |
           Agent Worker
```

## Implemented

- Windows capability detection
- working-directory validation
- Windows-only process adapter
- new-process-group creation for worker processes
- graceful termination with forced-kill fallback
- Named Pipe endpoint contract
- Windows-only Named Pipe capability detection
- transport details kept outside the gateway and agent layers

## Boundary

The process adapter creates and terminates processes. The process manager owns lifecycle state. The gateway owns transport-neutral routing. The sandbox owns policy and resource contracts.

## Security

Phase 23 does not claim privileged isolation. Process groups and termination are lifecycle controls, not a security sandbox. Windows Job Objects, restricted tokens, filesystem ACLs, network controls, and stronger containment remain explicit future adapters.

## Cross-platform policy

The AIOS core remains platform-neutral. Windows behavior lives under `aios.runtime`; Linux/macOS adapters can implement the same concepts without changing agent identity, A2A, gateway, or orchestration code.
