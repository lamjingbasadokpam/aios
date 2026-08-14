# AIOS Core Contracts

**Version:** 1.0
**Status:** Frozen conceptual contracts

These contracts define the minimum semantics of the ten AIOS primitives. The first implementation may refine exact Python typing without changing the concepts.

## Agent

An Agent is an identifiable autonomous actor with a lifecycle, instructions, capabilities, memory access, model preferences, and execution policy.

Minimum concepts:

```text
AgentId
name
version
status
capabilities
policy_ref
model_requirements
memory_policy
skill_refs
metadata
```

## Task

A Task is a unit of work with lineage, lifecycle, input, constraints, outputs, and execution context.

Minimum concepts:

```text
TaskId
parent_task_id
agent_id
status
input
constraints
requirements
environment_ref
created_at
started_at
completed_at
result
error
```

## Model

A Model exposes inference capabilities through a provider-independent interface.

Minimum concepts:

```text
ModelId
provider
capabilities
locality
context_limit
resource_requirements
health
```

Operations conceptually include:

```text
generate()
stream()
embed()
inspect_capabilities()
```

Not every model supports every operation.

## Memory

Memory is persisted or temporary information with provenance and lifecycle policy.

Minimum concepts:

```text
MemoryId
kind
content
metadata
provenance
trust
created_at
updated_at
retention
```

Conceptual operations:

```text
store()
retrieve()
search()
update()
invalidate()
delete()
```

## Tool

A Tool is an executable capability with an explicit schema and security requirement.

Minimum concepts:

```text
ToolId
name
description
input_schema
output_schema
required_capabilities
risk_level
network_requirements
filesystem_requirements
version
health
```

Conceptual operation:

```text
invoke(input, execution_context)
```

## Worker

A Worker is execution capacity.

Minimum concepts:

```text
WorkerId
capabilities
resources
health
status
locality
environment_support
```

Conceptual operations:

```text
submit()
cancel()
inspect()
```

## Resource

A Resource is allocatable capability or capacity.

Minimum concepts:

```text
ResourceId
type
capacity
available
capabilities
health
locality
```

Conceptual operations:

```text
allocate()
reserve()
release()
inspect()
```

## Event

An Event records a system fact.

Minimum concepts:

```text
EventId
type
timestamp
source
actor_id
task_id
correlation_id
payload
severity
provenance
```

## Policy

A Policy determines whether an action or resource request is allowed, denied, or requires approval.

Conceptual operation:

```text
evaluate(subject, action, resource, context) -> decision
```

Possible decisions:

```text
ALLOW
DENY
REQUIRE_APPROVAL
```

## Environment

An Environment bounds execution.

Minimum concepts:

```text
EnvironmentId
workspace
filesystem_policy
network_policy
tool_allowlist
model_allowlist
resource_limits
credential_refs
isolation_level
status
```

Conceptual operations:

```text
create()
start()
inspect()
stop()
destroy()
```

## Contract rules

1. IDs are stable within their lifecycle scope.
2. Lifecycle state transitions are explicit.
3. Failures are typed and observable.
4. Security decisions are auditable.
5. External implementations map into these contracts through adapters.
6. Contracts should be serializable where persistence or remote execution requires it.
7. Core contracts must not expose provider-specific objects as mandatory fields.
