# AIOS Markdown System

**Version:** 1.0
**Status:** Frozen

Markdown is the human-readable knowledge, instruction, skill, and architecture layer of AIOS.

## What Markdown is for

- system principles
- architecture
- agent definitions
- skills
- operational procedures
- knowledge notes
- policies that benefit from human review
- architecture decision records
- task notes

## What Markdown is not for

Markdown must not be the only representation of:

- mutable runtime state
- locks
- resource allocations
- credentials
- event delivery state
- high-frequency telemetry
- transactional data

Those belong in structured runtime stores.

## Agent definition

An `AGENT.md` should describe an agent's purpose, role, allowed capabilities, preferred model capabilities, memory behavior, operating constraints, and references to skills.

## Skills

A skill is a reusable procedural capability. A skill may contain Markdown instructions plus scripts, schemas, tests, or supporting assets.

## Knowledge

Knowledge Markdown may be indexed into Memory Fabric. Indexing should preserve file path, version/hash, source, and provenance.

## Policy

Human-readable policies can be stored as Markdown but enforcement must occur through machine-readable policy evaluation. Documentation alone does not enforce a security boundary.

## Loading discipline

The runtime should retrieve only relevant Markdown content instead of injecting the entire `.aios/` tree into every context.
