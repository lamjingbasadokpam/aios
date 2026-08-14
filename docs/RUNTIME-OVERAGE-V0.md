# AIOS Runtime Overage Enforcement V0

Phase 56 turns resource overages into explicit runtime decisions.

```text
Settlement
    |
    +--> SETTLED ------> ALLOW
    |
    +--> OVERAGE ------> OverageGuard
                              |
                         +----+----+
                         |         |
                      within     beyond
                      grace      grace
                         |         |
                       WARN    configured action
                                  |
                              STOP / WARN / ALLOW
```

## Policy

`OveragePolicy` supports an enforcement action plus optional grace for tokens, runtime, tool calls, retries, and cost.

The default action is `STOP` with zero grace, making the guard fail closed.

## Boundary

The guard decides what should happen; it does not itself terminate Python tasks. Execution adapters must translate `STOP` into cooperative cancellation or another safe runtime-specific stop mechanism.

Overage is not authorization. Capability policy remains a separate decision boundary.
