# AIOS Sandbox + Resource Isolation V0

Phase 16 adds a portable sandbox contract between agents and machine capabilities.

```text
Agent
  |
  v
Policy
  |
  v
SandboxSpec
  |
  +--> filesystem scopes
  +--> network intent
  +--> environment
  +--> runtime limits
  |
  v
OS/container adapter
  |
  v
Machine
```

## V0 controls

- explicit read paths
- explicit write paths
- network intent flag
- environment allowlist data
- runtime limit contract
- output-size limit

The reference runtime currently enforces filesystem scopes and output size. Runtime, memory, CPU, and network limits are contracts for future OS/container adapters.

## Important security boundary

A sandbox contract is not the same thing as a security sandbox. Python path checks alone cannot contain a malicious process. Production enforcement must happen below the agent runtime using OS primitives or a container/VM boundary.

Recommended future adapters:

- Windows Job Objects / restricted process tokens
- Linux namespaces/cgroups/seccomp
- containers
- microVMs for higher-risk workloads

## Per-agent isolation

```text
Agent A -> Sandbox A -> workspace A
Agent B -> Sandbox B -> workspace B
Agent C -> Sandbox C -> workspace C
```

Agents should not share writable state by default. Shared resources should be explicit capabilities.
