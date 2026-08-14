# AIOS Agent Manifest V0

Phase 26 makes agent execution profiles declarative and loadable from YAML.

```text
agent.yaml
   |
Manifest Loader
   |
Validation
   |
AgentExecutionProfile
   |
Runtime / Process Manager / Gateway
```

## Example

```yaml
id: researcher
model:
  provider: local
  name: qwen
sandbox: restricted
resources:
  processes: 3
  memory_bytes: 4294967296
  cpu_time_seconds: 120
network: true
tools:
  - filesystem.read
  - web.search
transport:
  type: ipc
```

## Design rules

- YAML is configuration, not executable policy.
- The loader converts configuration into the typed `AgentExecutionProfile` contract.
- Runtime layers remain responsible for enforcement.
- Unknown/unsafe execution behavior must not be inferred from arbitrary manifest fields.
- Provider/model names are identifiers; credentials and secrets do not belong in manifests.

## V0 scope

The loader supports YAML text/files, model provider/name mapping, resources, network policy, tools, transport, environment, and metadata. PyYAML is an optional runtime dependency for manifest loading.
