# AIOS Tool Fabric

**Version:** 1.0
**Status:** Frozen

## Purpose

Tool Fabric is the governed action boundary between agents and external capabilities.

## Tool classes

- native AIOS tools
- MCP tools
- browser tools
- computer-use tools
- remote tools

## Invocation pipeline

```text
Agent
 -> Tool Discovery
 -> Tool Registry
 -> Schema Validation
 -> Capability / Policy Check
 -> Tool Gateway
 -> Sandbox / Environment
 -> Tool Execution
 -> Result Validation
 -> Normalization
 -> Agent
```

## Tool manifest

A tool should declare at least:

- stable identifier
- name and description
- input schema
- output schema
- capabilities required
- risk level
- network access
- filesystem access
- authentication requirements
- sandbox/environment requirements
- version
- health information

## MCP boundary

MCP is an adapter/protocol layer for interoperable tool/resource/prompt integrations. AIOS may consume local or remote MCP servers but does not define itself as an MCP server.

## Browser and computer use

Browser automation and computer use are separate capability classes because they have different state, isolation, and security requirements. Browser sessions should be isolated from the user's personal browser profile by default.

## Tool discovery

The registry should support semantic and metadata-based discovery so agents do not receive every available tool schema in every context.

## Tool output safety

External tool results are untrusted data unless explicitly classified otherwise. Results should be normalized, size-limited where appropriate, provenance-tagged, and kept separate from system/user instructions.

## Tool health

The registry should track availability, latency, error rate, version, and authorization state. The runtime may select a fallback tool when policy permits.
