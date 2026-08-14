# AIOS Worker Fabric

**Version:** 1.0
**Status:** Frozen

## Purpose

Worker Fabric provides execution capacity to AIOS. V1 runs locally on Windows while the contract permits future remote and cloud workers.

## Worker model

A Worker reports capabilities such as:

- CPU capacity
- RAM
- GPU/VRAM
- operating system/runtime
- available environments
- network characteristics
- available tools
- health
- current load

## Worker lifecycle

```text
DISCOVERED -> REGISTERED -> READY -> BUSY -> READY
                         |                 |
                         +-> UNHEALTHY <-+
                         |
                         +-> OFFLINE
```

## Scheduling

The Scheduler chooses a worker using task requirements, resource availability, locality, policy, priority, health, and workload.

## Execution boundary

Workers should execute work through an Environment where isolation is required. Host-level execution is an explicit capability, not the default.

## Future scaling

The same Worker interface can represent:

- local Windows worker
- WSL worker
- Docker worker
- another machine
- dedicated server
- cloud VM/container/GPU worker

The V1 implementation should not introduce distributed coordination until local execution is reliable.
