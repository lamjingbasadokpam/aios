# AIOS Repository Structure

**Version:** 1.0
**Status:** Frozen for V1

The repository separates stable contracts, runtime implementation, adapters, infrastructure, tests, and human-readable AIOS state.

```text
aios/
├── README.md
├── pyproject.toml
├── LICENSE
├── .gitignore
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── PRINCIPLES.md
│   ├── COMPONENTS.md
│   ├── CORE-CONTRACTS.md
│   ├── REPOSITORY-STRUCTURE.md
│   ├── AGENT-RUNTIME.md
│   ├── MODEL-FABRIC.md
│   ├── MEMORY-FABRIC.md
│   ├── TOOL-FABRIC.md
│   ├── WORKER-FABRIC.md
│   ├── SECURITY.md
│   ├── ORCHESTRATION.md
│   ├── EVENTS.md
│   ├── RESOURCES.md
│   ├── MD-SYSTEM.md
│   ├── ROADMAP.md
│   ├── DECISIONS.md
│   └── decisions/
│
├── src/
│   └── aios/
│       ├── kernel/
│       ├── control/
│       ├── runtime/
│       ├── model/
│       ├── memory/
│       ├── tools/
│       ├── workers/
│       ├── environments/
│       ├── security/
│       ├── events/
│       ├── resources/
│       ├── config/
│       └── cli/
│
├── adapters/
│   ├── models/
│   ├── memory/
│   ├── tools/
│   ├── workers/
│   └── environments/
│
├── tests/
│   ├── unit/
│   ├── contract/
│   ├── integration/
│   └── end_to_end/
│
├── scripts/
│
└── .aios/
    ├── system/
    ├── agents/
    ├── skills/
    ├── knowledge/
    ├── memory/
    ├── tasks/
    ├── environments/
    └── policies/
```

## Package responsibilities

### `src/aios/kernel`

Stable low-level runtime primitives: identity, lifecycle, configuration boundary, state, registry, and kernel APIs.

### `src/aios/control`

Orchestration, scheduling, task coordination, delegation, and registry coordination.

### `src/aios/runtime`

Agent lifecycle and execution loop.

### `src/aios/model`

Provider-independent model contracts, routing, capability metadata, and model sessions.

### `src/aios/memory`

Memory contracts, retrieval, indexing, provenance, and context assembly.

### `src/aios/tools`

Tool contracts, discovery, invocation, schemas, and tool gateway behavior.

### `src/aios/workers`

Worker contracts, health, resource reporting, and dispatch.

### `src/aios/environments`

Execution environments and isolation boundaries.

### `src/aios/security`

Capabilities, policies, identity, approvals, secrets boundary, and audit interfaces.

### `src/aios/events`

Event contracts, bus, subscriptions, and persistence abstraction.

### `src/aios/resources`

Resource descriptors, allocation, reservation, and release.

### `src/aios/config`

Typed configuration loading and validation. Secrets should be referenced, not embedded in source-controlled config.

### `src/aios/cli`

Human-facing command-line interface. The CLI is a client of the control plane rather than the kernel itself.

### `adapters/`

Concrete integrations with external technologies. Adapters must depend on AIOS contracts rather than forcing external abstractions into the core.

### `tests/`

- `unit`: isolated implementation behavior
- `contract`: guarantees between interfaces and adapters
- `integration`: real subsystem combinations
- `end_to_end`: user-visible workflows

### `.aios/`

The machine-local AIOS workspace containing human-readable agents, skills, knowledge, policies, task artifacts, and runtime-managed state references. It is not the Python package.

## Dependency rule

```text
core contracts
     ↑
subsystem implementations
     ↑
adapters / infrastructure
     ↑
CLI / applications
```

Adapters may depend on contracts. Core packages must not import concrete adapters.

## V1 language choice

The initial runtime is specified as Python because the AI/agent ecosystem, local model tooling, async execution, and rapid systems iteration make it practical for V1. This is an implementation decision, not a requirement of the conceptual architecture.
