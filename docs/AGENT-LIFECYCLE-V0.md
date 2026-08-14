# AIOS Agent Lifecycle Controller V0

Phase 28 connects the agent registry and process manager through one lifecycle control surface.

```text
Agent Registry + Profile
          |
          v
Lifecycle Controller
   |      |       |
 start   stop   restart
   |      |       |
   +------v-------+
      Process Manager
           |
      OS Runtime Adapter
```

## Responsibilities

The controller coordinates identity/configuration and lifecycle state. It does not directly create Windows processes, enforce sandboxing, or implement IPC. Those remain OS/runtime responsibilities.

## V0 operations

- register an agent record
- start a registered/enabled agent after an external runtime provides its PID/endpoint
- stop
- restart
- report status
- record failures

## Why the PID is supplied by the runtime

This keeps the lifecycle layer portable and deterministic. A future launcher will create the worker through the Windows/Linux/cloud runtime and then report the resulting process handle/endpoint to the controller.

## Next integration

The lifecycle controller is intentionally ready for a launcher. The next layer can translate an `AgentExecutionProfile` into an OS launch request, apply resource/sandbox policy, establish transport, and then hand the resulting process identity back to this controller.
