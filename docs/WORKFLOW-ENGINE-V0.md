# AIOS Workflow Engine V0

Phase 43 adds a workflow identity and lifecycle state around the bounded plan executor.

```text
Workflow
  |
  v
WorkflowState
  |
  v
PlanExecutor
  |
  +--> completed_steps
  +--> failed_steps
  +--> step results
  |
  v
SUCCEEDED / FAILED
```

## Scope

A workflow wraps a validated `Plan` with a stable workflow ID and metadata. `WorkflowState` tracks lifecycle status and step outcomes.

V0 is intentionally in-memory and synchronous at the state layer. Persistence, pause/resume checkpoints, branching, scheduling, and event-driven execution are future concerns.

## Safety

Workflow execution still delegates actual capability execution to `PlanExecutor` and its `StepExecutor`. The workflow layer does not grant new permissions.

## Idempotence

A workflow already marked `SUCCEEDED` is treated as complete and is not executed again by the runner.
