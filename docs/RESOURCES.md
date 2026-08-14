# AIOS Resource Model

**Version:** 1.0
**Status:** Frozen

## Purpose

Resources are first-class objects that can be discovered, described, allocated, reserved, consumed, released, and monitored.

## Resource types

Examples include:

- CPU
- RAM
- GPU
- VRAM
- model instances
- workers
- tools
- memory stores
- environments
- browser sessions

## Resource descriptor

A resource should expose stable identity, type, capabilities, capacity, availability, health, locality, and policy metadata.

## Allocation

Tasks should express requirements declaratively when possible.

```text
requirements:
  gpu: true
  vram_min_gb: 12
  locality: local
  network: disabled
```

The Scheduler/Resource system finds a compatible allocation.

## Reservation

Long-running tasks may reserve resources. Reservations must expire or be released when a task terminates.

## Accounting

Resource accounting should eventually support usage, limits, quotas, and cost metadata without coupling the core resource contract to a billing system.

## Health

Resources can become degraded or unavailable. Consumers should receive typed failures rather than assuming availability.
