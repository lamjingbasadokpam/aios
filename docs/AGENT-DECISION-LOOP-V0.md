# AIOS Agent Decision Loop V0

Phase 33 adds the framework-neutral model/tool feedback loop that turns a model call into agentic execution.

```text
             Agent Loop
                 |
                 v
              Model
                 |
          tool call / final
             /        \
            v          v
          Tool        Final
            |
         result
            |
            +-----> Model
```

## Contract

The loop receives a model provider, model identifier, initial messages, a model response parser, and a maximum step count.

A parser returns either:

- `final`: terminate with generated content
- `tool_call`: execute the named tool and append the observation to history

## Safety properties

- Tool execution still passes through `ToolFabric` and therefore its existing gateway/policy boundary.
- A maximum step count prevents an unbounded tool loop.
- Provider SDKs remain outside the loop.
- The parser is injected so different model/tool-call formats can be supported without changing orchestration.

## V0 limitations

This is intentionally a small orchestration primitive. It does not yet implement planning, memory, streaming, parallel tool calls, human approval, retries, budgets, or durable checkpoints. Those belong to later orchestration layers.
