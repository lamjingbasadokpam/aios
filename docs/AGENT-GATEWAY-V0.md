# AIOS Agent Gateway V0

Phase 20 separates A2A message semantics from the transport used to move messages between runtimes.

```text
Agent
  |
  v
Agent Gateway
  |
  +-- in-process
  +-- IPC
  +-- HTTP
  +-- WebSocket
  |
  v
Remote/local runtime
```

## Envelope

A gateway envelope carries sender, recipient, payload, transport, request ID, optional correlation ID, and transport headers.

## Design rule

Agents and orchestration code should not depend directly on HTTP, WebSocket, sockets, or a vendor RPC SDK. They submit an envelope to the gateway and a transport adapter performs delivery.

## V0 scope

The gateway currently provides a transport registry and routing abstraction. Concrete network transports are intentionally not bundled yet. This keeps the protocol boundary stable before committing AIOS to one networking stack.

## Production direction

- local IPC for same-machine runtimes
- HTTP for request/response APIs
- WebSocket or streaming RPC for long-lived sessions
- authenticated agent identity at the gateway boundary
- correlation and tracing propagation
- retries and timeouts
- rate/resource limits
- encrypted transport for remote agents

The gateway should eventually become the only network-facing boundary for agent communication.
