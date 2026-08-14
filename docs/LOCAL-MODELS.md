# AIOS Local Models

## Phase 2.5

AIOS now has a real local-model adapter boundary through Ollama.

```text
AIOS ModelRouter
      |
      v
OllamaProvider
      |
      v
http://127.0.0.1:11434
      |
      v
Local Ollama model
```

## Install the runtime

Install Ollama separately on the host using its official distribution. AIOS does not bundle the runtime or automatically install models.

After the Ollama service is running, verify it from the host and make sure at least one model has been downloaded.

## AIOS behavior

When `OllamaProvider` is registered:

1. AIOS queries Ollama's local model list.
2. Each discovered model becomes an AIOS `Model`.
3. Models are marked `local`.
4. `ModelRouter` can select them using locality and capability requirements.
5. Inference is sent through the provider adapter.

If Ollama is unavailable, discovery returns no Ollama models instead of preventing the entire AIOS process from starting.

## Security boundary

The default endpoint is loopback only. AIOS should not expose Ollama's service publicly. Remote Ollama access, authentication, and network policy are future infrastructure concerns.

## Current limitations

- streaming is not implemented in the adapter yet
- capability metadata is conservative and will be refined per model/runtime
- no automatic model pulling
- no GPU/resource scheduler integration
- no token budget enforcement
- no cloud fallback

These limitations are intentional. The provider boundary comes first; advanced runtime behavior will be added above it.
