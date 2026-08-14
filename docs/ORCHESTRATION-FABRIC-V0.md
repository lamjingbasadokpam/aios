# AIOS Orchestration Fabric V0

## Purpose

Orchestration turns individual agent/task executions into dependency-aware workflows.

```text
Workflow
  |
  v
TaskGraph
  |
  v
Orchestrator
  |
  +--> ready tasks
  +--> concurrency limit
  +--> retries
  +--> dependency propagation
  |
  v
Task handlers / Agents
```

## V0 capabilities

- Directed task dependency graph
- Missing-dependency validation
- Cycle detection
- Bounded concurrency
- Per-task retries
- Failure propagation
- Shared execution context
- Normalized task results

Independent tasks can run concurrently up to `max_concurrency`.

```text
A ──────> C

B ──────> C
```

A and B may run in parallel. C starts only after both succeed.

## Why this is not yet a multi-agent framework

A task handler can eventually wrap `AgentRuntime`, but V0 deliberately keeps orchestration independent of agent implementation.

```text
Orchestrator
    |
    +--> normal function
    +--> AgentRuntime
    +--> remote/cloud worker
    +--> human approval task
```

This separation allows AIOS to scale execution without coupling the scheduler to a particular LLM framework.

## Future layers

- persistent workflow state
- event-driven scheduling
- cron/scheduled agents
- durable queues
- distributed workers
- agent delegation
- dynamic task generation
- cancellation and deadlines
- checkpoint/resume
- human approval nodes
- priority scheduling
- resource-aware placement

Those belong above this V0 contract.
