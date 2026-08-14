# AIOS Execution Fabric V0

AIOS can now execute an explicitly allowlisted process through a bounded executor.

```text
Agent
  |
  v
ToolGateway
  |
  v
process.execute
  |
  v
ProcessExecutor
  |
  +--> executable allowlist
  +--> workspace boundary
  +--> timeout
  +--> output limit
  +--> controlled environment
  |
  v
Process
```

## V0 guarantees

- Executables must be explicitly allowlisted.
- Working directories must remain inside the configured workspace.
- A caller cannot request a timeout above the executor limit.
- A caller cannot request output above the executor limit.
- Timeout results are normalized and the process is terminated.
- stdout/stderr are returned through `ExecutionResult`.

## What V0 does NOT guarantee

This is not yet a hardened OS sandbox. It does not provide complete isolation against a malicious process that is already allowed to execute. In particular, it does not yet implement Windows Job Objects, Linux namespaces/cgroups, containers, VMs, syscall filtering, or network namespace isolation.

The allowlist and workspace boundary are therefore policy controls, not a substitute for OS-level sandboxing.

## Why this is still useful

The execution contract is now separated from the Agent Runtime. Stronger backends can later implement the same contract:

```text
ProcessExecutor
   |
   +-- NativeBoundedExecutor
   +-- ContainerExecutor
   +-- WindowsSandboxExecutor
   +-- LinuxSandboxExecutor
   +-- VMExecutor
```

The agent does not need to know which backend is used.

## Next security work

Before enabling unattended high-risk execution, AIOS should add OS-level isolation and a credential/network policy layer.
