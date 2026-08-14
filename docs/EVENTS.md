# AIOS Event System

**Version:** 1.0
**Status:** Frozen

## Purpose

Events provide an observable record of important system activity and enable subscriptions, automation, debugging, and future distributed coordination.

## Event envelope

An event should contain, where applicable:

- event id
- event type
- timestamp
- actor/agent identity
- task id
- parent/correlation id
- source subsystem
- payload
- provenance
- severity

## Event classes

Examples:

```text
agent.*
task.*
model.*
memory.*
tool.*
worker.*
resource.*
policy.*
environment.*
security.*
```

## Delivery

The event system should distinguish transient operational events from events that must be durably retained for audit or recovery.

## Event consumers

Potential consumers include:

- CLI/UI
- audit store
- task monitor
- metrics
- automation rules
- debugging/replay tools

## Event discipline

Events should describe facts about what happened. They should not become an uncontrolled second configuration system.
