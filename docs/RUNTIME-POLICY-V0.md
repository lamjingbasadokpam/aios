# AIOS Runtime Policy / Governance V0

Phase 50 establishes the policy decision boundary between an agent's requested action and capability execution.

```text
Agent / Workflow
      |
      v
 PolicyRequest
      |
      v
    Policy
      |
      v
PolicyDecision
   /       \
 ALLOW     DENY
   |         |
   v         x
Execution
```

## V0

`AllowListPolicy` requires an explicit capability/action rule. Unknown capabilities and actions are denied by default.

## Architectural rules

- Policy evaluates intent; it does not execute tools.
- Authorization is separate from runtime control (`pause`, `resume`, `cancel`).
- A policy decision is explicit and carries a reason and policy identifier.
- Provider-specific identity, approval UI, budgets, rate limits, and sandbox enforcement are future policy adapters/layers.
- Default-deny is the safe baseline for capabilities.

Existing tool-level policy enforcement remains intact; this phase adds the runtime governance contract rather than replacing the established tool gateway.
