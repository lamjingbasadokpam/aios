# AIOS Windows Runtime V0

Phase 23 introduces the Windows-specific execution boundary without leaking Windows APIs into the AIOS core.

```text
AIOS Core
   |
Runtime Adapter
   |
Windows Runtime
   +-- capability detection
   +-- working-directory validation
   +-- command construction
   +-- future process adapter
   +-- future Named Pipe adapter
```

## V0 boundary

The adapter deliberately does not spawn arbitrary processes or claim security isolation. Those operations belong to explicit process, IPC, and sandbox adapters.

## Production direction

The Windows implementation should eventually provide:

- subprocess lifecycle integration with the Phase 22 process manager
- Windows Named Pipes for local agent transport
- Job Objects/resource controls where appropriate
- environment and working-directory isolation
- graceful termination and crash reporting
- integration with the Phase 16 sandbox policy

The platform adapter should remain replaceable so Linux and macOS runtimes can implement equivalent contracts.
