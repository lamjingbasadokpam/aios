# AIOS Tool Fabric V0

Phase 32 establishes the provider-neutral tool execution boundary while preserving the existing ToolGateway capability enforcement.

```text
Agent / LLM
    |
    v
Tool Fabric
    |
    v
ToolGateway
    |
    +--> capability check
    +--> tool registry
    |
    v
Tool Adapter / Handler
    |
    v
bounded environment
```

## Contract

`ToolRequest` identifies a registered tool and carries structured arguments. `ToolResponse` carries success, result/error, and metadata.

## Design rules

- Tools are explicitly registered; arbitrary names cannot execute capabilities.
- The fabric routes requests but does not replace the existing security gateway.
- Tool adapters must remain constrained by runtime sandbox and policy layers.
- Secrets do not belong in tool requests.
- The same contract can back local tools or remote/cloud capabilities.

## Agentic AI boundary

The model may propose a tool call, but the ToolGateway remains the authorization boundary. Model output never becomes implicit operating-system authority.

The existing V0 filesystem tools remain workspace-bounded; unrestricted shell, network, browser automation, MCP transport, and automatic approvals remain deferred to later phases.

## V0 scope

Registration, discovery, structured requests, routing, and normalized responses. Authorization continues to live in ToolGateway and policy, keeping execution and security separate.
