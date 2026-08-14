# AIOS Security Architecture

**Version:** 1.0
**Status:** Frozen

## Security model

AIOS uses capability-based, policy-driven security. An agent is not trusted merely because it is autonomous or locally hosted.

## Security dimensions

- identity
- capabilities
- permissions
- trust
- secrets
- filesystem access
- network access
- sandboxing
- approval
- audit

## Capability principle

```text
Agent identity
 -> requested capability
 -> policy evaluation
 -> allow / deny / require approval
 -> execution
```

Examples of capabilities:

`filesystem.read`, `filesystem.write`, `process.execute`, `network.request`, `browser.control`, `credential.use`, `system.control`.

## Risk levels

A V1 policy model should distinguish at least:

```text
READ
LOW
MEDIUM
HIGH
CRITICAL
```

High-risk operations should be gated by explicit policy. Destructive host operations and credential access should not be silently granted to arbitrary agents.

## Secrets

Agents should not receive raw credentials in normal model context. Tools should obtain credentials through a credential broker subject to policy.

## Network

Network access should be controllable by environment and policy. Domain, protocol, destination, rate, and data-transfer rules may be introduced progressively.

## Filesystem

Agents should operate inside explicit workspace boundaries by default. Host-wide filesystem access is a separate capability.

## Trust and provenance

Content from external websites, documents, tool outputs, and remote services should be classified as untrusted or externally sourced unless policy establishes otherwise.

External content must not silently override system or user instructions.

## Browser security

Autonomous browser sessions should use dedicated profiles/environments rather than the user's personal browser profile by default.

## Audit

Security-relevant decisions should produce structured events containing the actor, requested capability, policy result, resource, timestamp, and relevant task lineage.

## Human approval

Approval is policy-driven rather than requested for every action. Repetitive low-risk actions can be automatic; high-impact actions may require explicit approval.
