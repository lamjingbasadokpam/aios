# AIOS Agent Runtime

**Version:** 1.0
**Status:** Frozen

## Purpose

The Agent Runtime is the execution engine for AIOS agents. It turns a Task into controlled model reasoning, resource selection, actions, verification, memory updates, and a final result.

## Agent lifecycle

```text
CREATED
  -> READY
  -> RUNNING
  -> WAITING
  -> RUNNING
  -> COMPLETED

Alternative terminal states:
FAILED
CANCELLED
EXPIRED
```

## Execution loop

```text
1. Observe task and environment
2. Assemble relevant context
3. Select model capability
4. Retrieve relevant memory
5. Plan next action(s)
6. Discover/select tools or delegation targets
7. Request policy authorization
8. Execute action
9. Validate and normalize result
10. Update context and memory
11. Verify progress
12. Continue, delegate, recover, or complete
```

## Context model

Context is assembled from typed sources:

- system policy
- agent definition
- task input
- relevant memory
- tool schemas/results
- environment state
- user instructions
- previous execution state

External tool content must be marked as data with provenance/trust metadata and must not silently become higher-priority instructions.

## Checkpoints

Long-running tasks should persist enough state to resume after interruption. A checkpoint should identify the task, agent, environment, relevant context/state references, completed actions, pending actions, and recovery metadata.

## Delegation

An agent may delegate a subtask to another agent through the Control Plane. Delegation must preserve task lineage, policy constraints, provenance, and cancellation semantics.

## Cancellation

Cancellation must propagate to active child tasks and execution environments unless a policy explicitly permits a cleanup phase.

## Recovery

The runtime should classify failures such as model failure, tool failure, worker failure, policy denial, timeout, malformed output, and environment failure. Recovery strategies include retry, alternate model, alternate tool, alternate worker, checkpoint resume, user escalation, and terminal failure.

## Framework boundary

An external agent framework can implement planning/reasoning loops behind an AIOS adapter. AIOS retains ownership of agent identity, task lifecycle, policies, resources, memory/tool contracts, events, and execution boundaries.
