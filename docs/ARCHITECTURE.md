# AIOS Architecture

**Version:** 1.0
**Status:** Frozen
**Date:** 2026-08-14

## 1. Purpose

AIOS is a local-first AI Agent Operating System for a personal machine. It provides a common runtime and control plane through which autonomous agents can use models, memory, tools, workers, resources, and execution environments under explicit security policies.

AIOS is not an LLM wrapper, a RAG application, an MCP server, or a single agent framework. Those are replaceable implementation components within the system.

## 2. Architectural principles

1. **Local-first:** the system must remain useful without cloud services when suitable local capabilities exist.
2. **Private-by-default:** sensitive data and credentials remain local unless an explicit policy permits external access.
3. **Provider-agnostic:** core contracts do not depend on a particular model vendor, vector database, agent framework, or tool protocol.
4. **Capability-based security:** agents receive explicit capabilities rather than unrestricted machine access.
5. **Sandbox-first execution:** risky or untrusted work executes inside controlled environments.
6. **Event-driven and observable:** significant lifecycle and execution changes produce structured events.
7. **Composable:** agents can combine models, memory, tools, and workers without knowing implementation details.
8. **Replaceable implementations:** interfaces are stable; adapters and infrastructure can change.
9. **Progressive autonomy:** low-risk operations can be automatic while high-risk operations require policy or human approval.
10. **Designed for scale, implemented locally first:** the V1 architecture must support future remote/cloud workers without requiring a distributed system on day one.

## 3. System topology

```text
                         AIOS
                          |
             +------------+------------+
             |                         |
        CONTROL PLANE             SECURITY PLANE
             |                         |
      +------+-------+          +------+-------+
      |      |       |          |      |       |
 Orchestrator Scheduler Registry Policy Trust Audit
      |      |       |
      +------+-------+
             |
          KERNEL
             |
     +-------+--------+
     |       |        |
   AGENTS RESOURCES EVENTS
     |
     +-----------+-------------+
     |           |             |
   MODEL       MEMORY         TOOL
   FABRIC      FABRIC         FABRIC
     |           |             |
     +-----------+-------------+
                 |
           WORKER FABRIC
                 |
        +--------+--------+
        |        |        |
      LOCAL    REMOTE    CLOUD
```

## 4. Core primitives

The architecture is centered on ten primitives:

| Primitive | Responsibility |
|---|---|
| Agent | Persistent or ephemeral autonomous actor with identity, policy, context, and capabilities |
| Task | Unit of requested work with lifecycle, inputs, outputs, constraints, and provenance |
| Model | Reasoning, generation, embedding, vision, speech, or other inference capability |
| Memory | Persisted knowledge or experience available to agents |
| Tool | Action or external capability callable by an agent |
| Worker | Execution capacity on which tasks or tools run |
| Resource | Consumable or allocatable capability such as CPU, GPU, model, memory, or worker |
| Event | Structured record of a state transition or significant occurrence |
| Policy | Rule governing access, execution, routing, security, and approval |
| Environment | Bounded execution context containing workspace, tools, credentials, network, and resources |

## 5. Control Plane

The Control Plane coordinates the system without implementing domain-specific work.

### Orchestrator

Responsible for decomposing and coordinating tasks, agent delegation, sequencing, parallelism, retries, fallback, and completion.

### Scheduler

Responsible for selecting workers and resources according to requirements, availability, priority, policy, and locality.

### Registry

Maintains discoverable metadata for agents, models, tools, workers, memory stores, environments, and policies.

## 6. AIOS Kernel

The kernel is intentionally small. It owns:

- identity and lifecycle primitives
- configuration loading
- system state
- event publication
- resource registration
- core registries
- the internal API/syscall boundary

The kernel must not directly depend on a specific LLM provider, LangChain, MCP implementation, vector database, browser framework, or UI.

## 7. Agent Runtime

The Agent Runtime executes the agent loop:

```text
OBSERVE -> UNDERSTAND -> PLAN -> SELECT -> ACT -> VERIFY -> MEMORIZE
```

Responsibilities:

- agent lifecycle
- context assembly
- model selection requests
- tool selection requests
- memory retrieval and writes
- planning and execution
- checkpoints
- cancellation and recovery
- result production

The runtime may use external agent frameworks through adapters, but AIOS owns the lifecycle and core contracts.

## 8. Model Fabric

Model access is abstracted behind provider-independent interfaces.

```text
ModelRegistry
     |
ModelRouter
     |
Provider Adapter
     |
+----+----------------+
|                     |
Local               Cloud
```

The router may consider capability, latency, privacy, cost, resource availability, context limits, and policy.

Initial implementations may include local runtimes such as Ollama or llama.cpp and cloud providers. These are adapters, not architectural dependencies.

## 9. Memory Fabric

Memory is divided into:

- working memory
- episodic memory
- semantic memory
- procedural memory
- durable knowledge

Retrieval may combine:

- vector similarity
- lexical/full-text search
- metadata filtering
- graph traversal
- temporal constraints
- provenance and trust

RAG is a retrieval mechanism within Memory Fabric, not the definition of memory.

All durable memory should retain provenance where practical.

## 10. Tool Fabric

Tool Fabric provides governed access to capabilities.

```text
Agent
  |
Tool Discovery
  |
Tool Registry
  |
Policy / Capability Check
  |
Tool Gateway
  |
Execution
  |
Validation / Normalization
  |
Result
```

Supported categories:

- native AIOS tools
- MCP tools
- browser tools
- computer-use tools
- remote tools

MCP is an integration protocol and is not the AIOS runtime.

## 11. Worker Fabric

Workers provide execution capacity. V1 targets one Windows machine but exposes a worker abstraction suitable for later remote execution.

Worker capabilities include CPU, GPU, memory, filesystem, network, sandbox/runtime support, and available tools.

## 12. Environment System

Tasks can execute inside an environment that defines:

- workspace
- filesystem boundaries
- available tools
- model access
- memory access
- browser session
- credentials
- network policy
- resource limits

Environments should be disposable where practical.

## 13. Security Plane

Security crosses every subsystem.

Core concepts:

- identity
- capability
- permission
- trust level
- secret access
- filesystem policy
- network policy
- sandbox policy
- approval policy
- audit

External content is data, not instruction. Tool outputs must retain source/trust metadata where possible.

## 14. Event System

Important state transitions are emitted as structured events. Examples include:

`agent.created`, `agent.started`, `agent.completed`, `task.created`, `task.failed`, `model.loaded`, `tool.invoked`, `tool.denied`, `worker.failed`, and `memory.created`.

Events support observability, debugging, replay, automation, and future distributed coordination.

## 15. Resource system

Resources are first-class and may be required, allocated, reserved, released, or unavailable.

Examples:

- CPU
- RAM
- GPU/VRAM
- model instances
- workers
- tools
- memory stores
- environments

Resource requirements must be declarative where practical so scheduling can evolve independently of agent logic.

## 16. Markdown layer

Markdown is the human-readable layer for architecture, principles, agent definitions, skills, knowledge, policies, decisions, and operational instructions.

Markdown is not the sole source of runtime state. Structured state belongs in appropriate stores.

Recommended future layout:

```text
.aios/
├── system/
├── agents/
├── skills/
├── knowledge/
├── memory/
├── tasks/
├── environments/
└── policies/
```

## 17. Framework boundaries

LangChain, LangGraph, OpenAI Agents SDK, MCP SDKs, browser-use, Playwright, Ollama, llama.cpp, vector databases, and similar technologies may be used behind AIOS interfaces.

No external framework is allowed to become the definition of an AIOS primitive.

## 18. V1 scope

V1 targets a useful autonomous agent on one Windows machine with:

- local and optional cloud model access
- persistent memory and retrieval
- governed native and MCP tools
- controlled browser/tool execution
- sandboxed work
- task orchestration
- event logging
- capability-based permissions
- Markdown-based skills and knowledge
- CLI-first operation

V1 explicitly excludes a full distributed cluster, enterprise IAM, unrestricted host-level computer control, and a large autonomous swarm.

## 19. Architecture change policy

Implementations may change without architecture revision. Changes to core primitives, subsystem boundaries, security boundaries, lifecycle contracts, or local-first assumptions require an Architecture Decision Record and versioned architecture update.
