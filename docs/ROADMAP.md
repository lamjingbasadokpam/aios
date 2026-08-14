# AIOS Implementation Roadmap

**Architecture baseline:** v1.0 frozen 2026-08-14

## Phase 0 — Specification

- architecture documents
- component boundaries
- core primitive definitions
- security model
- initial ADR process
- repository conventions

**Exit:** contracts are reviewable and implementation dependencies are explicit.

## Phase 1 — Kernel V0

Build the smallest executable core:

- configuration
- identity
- lifecycle
- event bus
- resource registry
- basic task model
- basic agent registry
- structured logging
- CLI skeleton

**Exit:** AIOS can start, register an agent, create a task, emit events, and shut down cleanly.

## Phase 2 — Model Fabric V0

- model interface
- provider registry
- one local provider
- one optional cloud provider
- basic capability-aware routing
- model health

**Exit:** an agent can request a model capability without depending on a provider-specific API.

## Phase 3 — Tool Fabric V0

- tool interface
- registry
- discovery
- policy checks
- native filesystem/process tools in a bounded workspace
- MCP adapter

**Exit:** an agent can discover and invoke governed tools with auditable events.

## Phase 4 — Memory Fabric V0

- working memory
- document ingestion
- lexical retrieval
- vector retrieval
- provenance
- context assembly

**Exit:** an agent can persist and retrieve useful knowledge without loading the entire knowledge base into context.

## Phase 5 — Environment + Worker V0

- local worker
- bounded workspace
- process execution
- Docker/WSL adapter where justified
- resource reporting
- environment lifecycle

**Exit:** tasks can execute reproducibly in a controlled local environment.

## Phase 6 — Agent Runtime V0

- agent lifecycle
- execution loop
- memory/tool/model integration
- checkpoints
- retries
- cancellation
- recovery

**Exit:** one autonomous agent can complete multi-step tasks reliably.

## Phase 7 — Orchestration V0

- sequential tasks
- parallel tasks
- delegation
- retries/fallbacks
- approval gates
- task graph persistence

**Exit:** multiple agents can collaborate through explicit task graphs without uncontrolled swarm behavior.

## Phase 8 — Browser / Computer Use

- isolated browser sessions
- browser tool adapter
- browser policy
- computer-use sandbox
- observation/action loop

**Exit:** controlled UI automation works without exposing the personal browser profile or unrestricted host access.

## Phase 9 — Scale-out

Only after local reliability:

- remote workers
- cloud workers
- distributed queues
- worker scheduling
- artifact transfer
- remote policy enforcement

**Exit:** an existing task can move from local to remote execution without changing agent contracts.

## Phase 10 — Advanced Agentic System

Potential future capabilities:

- long-running agents
- scheduled agents
- event-triggered agents
- advanced planning
- graph-based workflows
- specialized agent teams
- self-evaluation
- adaptive routing
- richer knowledge graphs

These are deliberately deferred until the foundational runtime is reliable.
