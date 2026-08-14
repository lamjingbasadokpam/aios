# AIOS Local Machine Runtime V0

Phase 15 establishes the machine boundary for local agents.

```text
Agent
  |
  v
CapabilityRequest
  |
  v
Policy
  |
  +--> ALLOW
  +--> DENY
  +--> APPROVAL_REQUIRED
  |
  v
Machine adapter
```

## Capabilities

V0 defines explicit capability names for:

- filesystem read/write
- process execution
- network access
- environment-variable reads

Only filesystem read and environment reads have reference runtime methods in V0. The other capabilities remain contracts until their adapters can be implemented with appropriate isolation.

## Default-deny

A capability is denied unless it is explicitly allowed. This is intentional: an LLM must never inherit the full permissions of the account running AIOS merely because it is an agent.

## Approval boundary

Policies can mark capabilities as requiring approval. A future UI/API can turn this into a human approval workflow without changing the agent contract.

## Security direction

```text
Agent
  |
Capability request
  |
Policy engine
  |
Sandbox / OS adapter
  |
Actual machine
```

Future versions should add path scopes, command allowlists, network egress rules, secret isolation, audit events, OS-level process isolation, and resource limits.

Do not expose unrestricted shell execution merely by adding `PROCESS_EXEC` to a policy. Process execution must be implemented through a constrained adapter.
