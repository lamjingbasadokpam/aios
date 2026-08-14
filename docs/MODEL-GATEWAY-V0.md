# AIOS Model Gateway V0

Phase 31 establishes the provider-neutral Generative AI boundary between an agent worker and model backends.

```text
Agent Worker
     |
     v
 Model Gateway
     |
  provider ID
     |
 +---+----------------+
 |                    |
Local adapter     Cloud adapter
 |                    |
Ollama/vLLM/etc.   API provider
```

## Contract

`ModelRequest` carries a model identifier, messages, and provider-neutral parameters. `ModelResponse` carries generated content, finish reason, usage, and metadata.

## Design rules

- The worker does not depend on a specific model SDK.
- Providers are explicitly registered and selected; no implicit fallback is performed.
- Credentials/secrets are not stored in model requests or agent manifests.
- Local and cloud providers use the same adapter contract.
- Streaming, tool calling, embeddings, and multimodal payloads are future extensions rather than hidden provider-specific behavior.

## Why this matters

AIOS can run the same agent against a local model for private/offline execution or a cloud model for higher capability without changing process, sandbox, lifecycle, or worker architecture.
