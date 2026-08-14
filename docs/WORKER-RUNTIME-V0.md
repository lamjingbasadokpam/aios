# AIOS Worker Runtime V0

Phase 30 defines the standardized runtime living inside an agent worker process.

```text
OS Process
   |
   v
AgentWorkerRuntime
   |
   +-- WorkerContext
   +-- operation dispatch
   +-- injected handler
   |
   +--> Model Runtime
   +--> Tool Fabric
   +--> Gateway / IPC
```

## Boundary

The worker runtime owns worker lifecycle and dispatch. It does not embed a specific model SDK, tool framework, or transport implementation.

## Lifecycle

`start -> dispatch* -> stop`

Dispatch before `start` is rejected. After `stop`, dispatch is rejected again.

## Why this abstraction exists

The same worker contract can host a local model, remote model API, LangChain-based agent, custom agent loop, or future cloud runtime without changing the process/sandbox/lifecycle layers.

## V0 scope

This phase establishes the typed worker context and asynchronous dispatch contract. Model invocation, tool execution, A2A protocol handling, persistent state, and streaming are separate layers and should be added through injected adapters rather than growing the worker core into a monolith.
