# AIOS Orchestration

**Version:** 1.0
**Status:** Frozen

## Purpose

Orchestration coordinates agents and tasks without coupling the system to a particular agent framework.

## Supported patterns

- sequential execution
- parallel execution
- conditional branching
- retries
- fallback
- delegation
- scheduled execution
- human approval gates

## Task graph

A task may be represented as a directed execution graph:

```text
Task
 |
 +--> Subtask A ----+
 |                  |
 +--> Subtask B ----+--> Subtask D
 |
 +--> Subtask C
```

The graph must retain parent/child lineage and policy constraints.

## Scheduler relationship

Orchestrator decides **what** should happen. Scheduler decides **where/when** available work should execute based on resources and policy.

## Retry

Retries should be bounded and failure-aware. A retry must not repeat a non-idempotent action blindly. Tool contracts should expose idempotency or compensation semantics where relevant.

## Parallelism

Parallel tasks must declare or imply resource requirements and should not violate shared-resource or data consistency constraints.

## Delegation

Delegated agents operate under inherited task constraints unless a policy explicitly grants additional capabilities. Child agents must not escape the parent's security boundary by default.

## Human gates

Approval nodes should be explicit task states and auditable events rather than hidden prompts inside individual tools.

## V1 approach

Start with a small reliable orchestrator supporting sequential, parallel, retry, delegation, and approval patterns. More advanced planning/swarm behavior is deferred until the core lifecycle is stable.
