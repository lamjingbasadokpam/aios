# AIOS Tool Fabric V0

## Purpose

Tool Fabric is the controlled bridge between an agent and executable capabilities on the machine.

```text
Agent / LLM
    |
    v
ToolGateway
    |
    +--> capability check
    |
    +--> tool registry
    |
    v
Tool Handler
    |
    v
bounded environment
```

## V0 components

- `Tool`: immutable capability metadata and schema
- `ToolContext`: execution identity and granted capabilities
- `ToolResult`: normalized result/error envelope
- `ToolRegistry`: discovery and handler lookup
- `ToolGateway`: invocation and capability enforcement

## Security rule

A model's ability to request a tool does not grant permission to execute it.

The gateway compares:

```text
required_capabilities
        vs
context.granted_capabilities
```

Missing capabilities produce a denial before the handler runs.

## Filesystem tools

V0 provides read/write text-file handlers restricted to an explicit workspace root.

They cannot traverse outside that root through `..` or resolved symlinks that escape the workspace.

## Why shell is not included yet

A general process/shell tool is much higher risk than bounded file operations. It requires a separate Environment and Policy layer for working-directory, executable allowlists, environment variables, network access, timeouts, process tree cleanup, and OS isolation.

Therefore shell execution is deferred until the Environment Fabric exists.

## MCP

MCP should later be implemented as a Tool adapter. It must still pass through the AIOS ToolGateway and security policy; an MCP server does not bypass AIOS permissions.

## Non-goals

V0 does not implement:

- arbitrary shell execution
- unrestricted filesystem access
- network tools
- browser automation
- automatic approvals
- MCP transport
- tool planning

Those belong to later phases.
