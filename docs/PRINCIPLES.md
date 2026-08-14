# AIOS Engineering Principles

**Version:** 1.0
**Status:** Frozen

## 1. Local-first

AIOS must be useful on a single personal machine. Cloud services enhance capability but are not architectural prerequisites.

## 2. Private-by-default

Data remains local unless a policy explicitly permits external transfer. Sensitive data should not enter model context merely because a tool can access it.

## 3. Capabilities over trust

Agents receive explicit capabilities. An agent's intelligence does not grant additional machine privileges.

## 4. Interfaces over implementations

Core contracts must not depend on a specific vendor, framework, database, model, or protocol implementation.

## 5. Sandbox-first

Untrusted code, high-risk operations, and external automation should execute inside bounded environments whenever practical.

## 6. Explicit provenance

AIOS should be able to answer where information came from, which agent produced it, which model generated it, and which tools were used.

## 7. Observable by default

Important operations emit structured events. Silent autonomous behavior is considered a debugging and security liability.

## 8. Progressive autonomy

Start with narrow capabilities and expand autonomy through tested policies rather than giving agents unrestricted access from the beginning.

## 9. Failure is normal

Tasks, tools, models, workers, and networks fail. Recovery, retry, fallback, checkpointing, and cancellation are first-class design concerns.

## 10. Mechanisms over documentation

Where a rule can be enforced by code, policy, schema, validation, or automation, prefer that mechanism over relying only on documentation.

## 11. Small kernel

Keep the kernel stable and minimal. Domain complexity belongs in higher-level fabrics and adapters.

## 12. Scale through composition

The architecture should scale by composing agents, workers, tools, memory, and models rather than by making every component globally intelligent.

## 13. Human-readable system

Important agent behavior, skills, policies, and architecture should remain inspectable in normal text formats, especially Markdown, without making Markdown the runtime database.

## 14. Replaceable intelligence

Models are resources, not identities. The system should be able to route a task among local and cloud models without changing agent logic.

## 15. Security boundaries are architecture

Identity, permissions, secrets, trust, sandboxing, network access, and approval are part of the architecture rather than later hardening.
