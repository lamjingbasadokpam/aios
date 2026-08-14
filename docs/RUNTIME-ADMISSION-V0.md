# AIOS Runtime Admission V0

Phase 53 composes runtime state, capability policy, and resource budgets into one fail-closed admission gate.

```text
Capability request
      |
      v
AdmissionController
      |
      +--> run state == RUNNING
      +--> Policy == ALLOW
      +--> Budget == ALLOW
      |
      v
    ADMIT
      |
      v
 Capability executor
```

Any failed prerequisite produces `DENY`. The controller does not execute the capability and does not grant permissions itself; it composes existing control and governance decisions.

V0 is intentionally synchronous at the decision boundary and in-memory. Durable distributed admission, reservations, concurrent usage accounting, and cooperative cancellation enforcement are later runtime concerns.
