# AIOS Model Fabric

**Version:** 1.0
**Status:** Frozen

## Purpose

Model Fabric provides provider-independent access to inference capabilities.

## Model abstraction

A model is described by capabilities and constraints, not merely a vendor name.

Representative capabilities:

- text generation
- reasoning
- code generation
- vision
- embeddings
- speech recognition
- speech synthesis
- structured output

Representative metadata:

- context limit
- modalities
- tool-calling support
- structured-output support
- latency class
- cost class
- locality
- resource requirements
- availability/health

## Provider boundary

```text
Agent Runtime
    -> Model Router
        -> Model Provider Interface
            -> Local Adapter / Cloud Adapter
```

Potential adapters include local runtimes and cloud APIs. No provider is required by the core architecture.

## Routing policy

Routing may consider:

1. required capability
2. privacy policy
3. locality requirement
4. model quality tier
5. context requirements
6. tool/structured-output support
7. latency
8. cost
9. GPU/VRAM availability
10. provider health

## Local-first behavior

When policy requires local execution, cloud providers must not be selected. When cloud is permitted, the router may use cloud models as fallback or as the selected capability when they provide a material advantage.

## Sessions

Inference sessions should expose lifecycle and usage metadata without forcing provider-specific session concepts into the core model.

## Model failure

A provider failure should be surfaced as a typed failure so the runtime can retry, select an alternate model, or escalate according to policy.
