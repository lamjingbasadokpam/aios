# AIOS Component Contracts

**Version:** 1.0
**Status:** Frozen

This document defines subsystem ownership. It intentionally describes contracts rather than implementation libraries.

## Kernel

Owns identity, lifecycle, configuration, core state, events, resources, and internal boundaries.

Must not own model-specific, database-specific, or UI-specific logic.

## Control Plane

Owns orchestration, scheduling, registry, task coordination, and policy evaluation requests.

## Agent Runtime

Owns agent lifecycle, execution loop, context assembly, delegation, checkpoints, recovery, and completion.

## Model Fabric

Owns model discovery, provider adapters, routing, inference sessions, capability metadata, and model resource accounting.

## Memory Fabric

Owns memory lifecycle, indexing, retrieval, ranking, provenance, persistence, and forgetting/retention policies.

## Tool Fabric

Owns tool discovery, registration, schema validation, capability checks, invocation, result normalization, and tool health.

## Worker Fabric

Owns execution workers, resource reporting, worker lifecycle, job dispatch, health, and environment execution.

## Environment System

Owns bounded task contexts, workspaces, browser sessions, filesystem/network boundaries, and environment teardown.

## Security Plane

Owns identity, capabilities, policy evaluation, secret brokering, trust metadata, audit, and approval workflows.

## Event System

Owns event schema, publication, subscriptions, persistence policy, and delivery guarantees appropriate to each event class.

## Resource System

Owns resource registration, capability descriptions, allocation, reservation, release, and health state.

## Dependency direction

Preferred direction:

```text
UI / CLI
  -> Control Plane
  -> Kernel contracts

Agent Runtime
  -> Model / Memory / Tool / Worker contracts

Fabrics
  -> Kernel contracts

Adapters
  -> Fabric contracts

Infrastructure
  -> Adapters
```

Lower layers must not import high-level application behavior merely to perform their infrastructure role.

## Adapter rule

External systems enter AIOS through adapters. Examples include:

- model provider adapter
- vector store adapter
- MCP adapter
- browser adapter
- sandbox adapter
- cloud worker adapter

An adapter may translate external concepts into AIOS primitives but must not redefine them.
