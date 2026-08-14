# AIOS Local IPC V0

Phase 21 adds the first concrete cross-process transport to the agent gateway.

```text
AIOS Process A
    |
Agent Gateway
    |
Unix-domain IPC
    |
AIOS Process B
```

The reference transport uses Python's asyncio Unix-domain socket server where the host supports it. Messages are newline-delimited JSON envelopes.

## Boundary

IPC is a transport adapter. Agents continue to depend on the gateway contract rather than sockets directly.

## Security

The socket path and OS permissions are part of the trust boundary. V0 does not yet implement remote authentication, encryption, capability negotiation, or hardened peer identity verification.

## Windows note

The current reference implementation targets Unix-domain socket support exposed by the Python runtime. Windows-native named-pipe transport should be added as a separate adapter rather than weakening the transport abstraction.

## Next reliability work

Add connection lifecycle handling, request timeouts, framing limits, authentication/peer identity, retries, backpressure, and integration with the durable A2A store.
