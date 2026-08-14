# AIOS Runtime Lifecycle V0

Phase 58 connects the runtime control, reservation, cancellation, and settlement primitives into one lifecycle boundary.

```text
CREATED
   |
   v
ADMITTED
   |
   v
RESERVED
   |
   v
RUNNING <------ cancellation request
   |
   v
SETTLING
   |
   +------> COMPLETED
   |
   +------> CANCELLED
```

## Lifecycle responsibilities

- `create()` registers the run.
- `admit()` establishes that the run may enter execution preparation.
- `reserve()` commits estimated resources before execution and transitions the run to `RUNNING`.
- `cancel()` records a provider-neutral cancellation request and moves the run to `CANCELLED`.
- `settle()` reconciles actual usage against the reservation and finalizes the run.

The lifecycle orchestrator intentionally does not execute tools or models. It coordinates runtime state; policy/admission and execution remain separate boundaries.

V0 is an in-memory orchestration layer. Durable lifecycle state, distributed reservations, event emission, and executor integration are subsequent concerns.
