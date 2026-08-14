# AIOS Architecture Decision Records

This file is the index for architecture decisions. Detailed decisions can be added under `docs/decisions/`.

## ADR-0001 — Local-first architecture

**Status:** Accepted

AIOS is designed to run usefully on one personal Windows machine. Cloud and remote execution are optional extensions.

## ADR-0002 — Ten core primitives

**Status:** Accepted

The stable conceptual primitives are Agent, Task, Model, Memory, Tool, Worker, Resource, Event, Policy, and Environment.

## ADR-0003 — Provider-agnostic boundaries

**Status:** Accepted

External model providers, databases, tool protocols, browser frameworks, and agent frameworks are adapters behind AIOS contracts.

## ADR-0004 — Capability-based security

**Status:** Accepted

Agent autonomy does not imply host privileges. Access is explicitly granted through capabilities and policies.

## ADR-0005 — MCP as integration protocol

**Status:** Accepted

MCP is supported through Tool Fabric but is not the definition of AIOS or the only tool mechanism.

## ADR-0006 — Markdown as human-readable layer

**Status:** Accepted

Markdown is used for inspectable architecture, agents, skills, knowledge, and policies. Runtime state and secrets remain in structured systems.

## ADR-0007 — Local implementation before distributed scale

**Status:** Accepted

Distributed workers and cloud orchestration are deferred until local execution is reliable. Interfaces must nevertheless preserve a clean path to scale-out.
