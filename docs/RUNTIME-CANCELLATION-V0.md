# AIOS Runtime Cancellation V0

Phase 57 establishes one provider-neutral cooperative cancellation contract.

```text
Control / Overage / Shutdown / Policy / Timeout
                     |
                     v
            CancellationRequest
                     |
                     v
             CancellationToken
                     |
          execution boundaries
                     |
                     v
              stop cooperatively
```

## Rules

- Cancellation is cooperative; the token does not forcibly terminate Python tasks.
- The first cancellation request wins, making repeated cancellation idempotent.
- Reasons are explicit: user, overage, shutdown, policy, and timeout.
- Executors and tools should check the token at safe boundaries and call `raise_if_cancelled()`.
- Cancellation is distinct from authorization: policy decides whether an action is permitted; cancellation stops an already-running execution.
