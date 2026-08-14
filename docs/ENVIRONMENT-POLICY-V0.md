# AIOS Environment & Policy Fabric V0

## Purpose

Phase 5 establishes the security boundary between agent intent and machine execution.

```text
Agent / LLM
     |
     v
ToolGateway
     |
     +--> capability check
     |
     +--> PolicyEngine
     |
     +--> Environment limits
     |
     v
Tool handler
```

## Environment

An `Environment` represents the execution context in which an agent is allowed to operate.

V0 tracks:

- capabilities
- workspace root
- maximum runtime
- maximum process count
- maximum output size
- network permission

The structure is intentionally independent of Docker, containers, VMs, or OS-specific sandboxes.

## Policy

`PolicyEngine` is the central decision point. A policy can:

- grant capabilities
- explicitly deny tools
- require approval for high-risk operations
- reject network operations in network-disabled environments

## Defense in depth

AIOS uses two checks:

1. `ToolContext.granted_capabilities` — what the current agent/task has been granted.
2. `PolicyEngine` + `Environment` — what the operating environment permits.

Both must allow the operation.

## Approval

High and critical risk tools can produce an `approval_required` decision. V0 exposes this decision to callers but does not yet provide a human approval UI or persistent approval token.

## Important limitation

Environment limits are metadata and policy constraints in V0; they are not yet OS-level isolation. A process sandbox, cgroup/job-object enforcement, container backend, or VM backend must be added before AIOS should expose arbitrary process execution to untrusted agents.

## Next security step

The next phase should implement a controlled process execution adapter with:

- explicit executable allowlist
- workspace-bound working directory
- environment-variable allowlist
- timeout
- output limit
- process-tree termination
- network policy enforcement

Only then should AIOS expose a general-purpose shell/process tool.
