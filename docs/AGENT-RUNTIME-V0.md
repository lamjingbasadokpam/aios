# AIOS Agent Runtime V0

## Purpose

The Agent Runtime is the execution layer that connects Tasks, Models, and Tools into a bounded agentic loop.

```text
Task
  |
  v
AgentRuntime
  |
  +--> ModelRouter --> ModelProvider
  |
  +--> ToolGateway --> Tool
  |
  +--> bounded loop
```

## V0 loop

1. Construct an inference request from the task and prior tool history.
2. Route the request through `ModelRouter`.
3. Require the model to return one structured action.
4. `final` ends the task.
5. `tool` invokes `ToolGateway`.
6. Append the normalized tool result to history.
7. Repeat until completion or `max_steps` is reached.

## Why the loop is bounded

Autonomy without a hard execution bound is unsafe and makes runaway tasks difficult to reason about. V0 therefore requires `max_steps`.

Future limits will include:

- wall-clock timeout
- token budget
- tool-call budget
- resource budget
- approval checkpoints
- cancellation

## Structured actions

V0 uses this minimal protocol:

```json
{"action":"final","answer":"..."}
```

or:

```json
{"action":"tool","tool_id":"filesystem.read","arguments":{"path":"notes/a.md"}}
```

This is intentionally an internal runtime protocol. A future model adapter may translate native function/tool calls into the same runtime action representation.

## Security

The runtime does not execute tools directly. Every tool request passes through `ToolGateway`, which enforces capabilities.

```text
LLM request
   |
   v
AgentRuntime
   |
   v
ToolGateway
   |
   v
Capability check
   |
   v
Tool
```

## V0 non-goals

- autonomous background agents
- multi-agent delegation
- persistent memory
- RAG
- planning graphs
- human approval UI
- arbitrary shell execution
- cloud failover
- LangChain dependency

Those are intentionally later layers.
