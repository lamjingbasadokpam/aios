# AIOS Agent Registry + Identity Fabric V0

Phase 17 makes agent identity a first-class concept separate from execution.

```text
Agent Identity (persistent)
        |
        +-- model
        +-- role
        +-- tools
        +-- memory namespace
        +-- sandbox profile
        +-- metadata
        |
        v
Worker (ephemeral)
        |
        v
Process
```

## V0

- stable UUID identity
- role/model configuration
- memory namespace binding
- sandbox profile binding
- tool declarations
- metadata
- enable/disable state
- duplicate-registration protection

The registry is currently an in-process reference implementation. Durable registry storage will be connected through the Storage Fabric in a later phase.

## Design rule

Workers do not own agent identity. A failed worker can be replaced while the same agent identity remains addressable.

This separation is required before implementing agent-to-agent messaging and local/cloud placement.
