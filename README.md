# AIOS — Local-First AI Agent Operating System

AIOS is a machine-level, local-first operating system for autonomous AI agents. It provides a common control plane for agents, tasks, models, memory, tools, workers, resources, events, policies, and execution environments.

## Architecture status

**Architecture Freeze: v1.0 — 2026-08-14**

The architecture is frozen at the interface and responsibility level. Implementations remain replaceable.

## Core principles

- Local-first
- Private-by-default
- Provider-agnostic
- Capability-based security
- Modular and replaceable implementations
- Observable and event-driven
- Sandbox-first execution
- Human approval for high-risk actions
- Design for future distributed/cloud execution without requiring it in V1

## Core primitives

`Agent` · `Task` · `Model` · `Memory` · `Tool` · `Worker` · `Resource` · `Event` · `Policy` · `Environment`

## Major subsystems

- AIOS Kernel
- Control Plane
- Agent Runtime
- Model Fabric
- Memory Fabric
- Tool Fabric
- Worker Fabric
- Environment System
- Security Plane
- Event System
- Resource System
- Markdown-based human knowledge and skills layer

## V1 goal

Run a useful autonomous agent on a single Windows machine that can reason with local or cloud models, retrieve knowledge, use governed tools, execute work in isolated environments, persist memory, and recover from failures.

V1 deliberately does **not** attempt to build a distributed cluster, unrestricted autonomous desktop controller, or enterprise IAM platform.

## Repository structure

The engineering specification is kept under `docs/`. Implementation will be derived from these contracts rather than invented ad hoc during coding.

## Architecture rule

Change implementations freely; change core contracts deliberately. Any change to kernel boundaries, core primitives, security boundaries, lifecycle, or major subsystem responsibilities requires an architecture decision record and versioned architecture change.
