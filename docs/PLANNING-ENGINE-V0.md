# AIOS Planning Engine V0

Phase 41 introduces a provider-neutral planning boundary between goals and execution.

```text
Goal + Context
      |
      v
    Planner
      |
      v
     Plan
      |
      v
 PlanValidator
      |
      v
 Executor (future phase)
```

## Contracts

- `Plan`: immutable goal plus ordered plan steps.
- `PlanStep`: description, stable ID, dependencies and metadata.
- `Planner`: pluggable planning implementation.
- `PlanValidator`: verifies dependency references before execution.

`StaticPlanner` is intentionally deterministic and only exists as a local contract implementation. A model-backed planner can later implement the same protocol.

## Safety boundary

Planning does not execute tools. A plan is data until a later execution/orchestration layer explicitly accepts it. This keeps generated plans separate from capabilities and authorization.
