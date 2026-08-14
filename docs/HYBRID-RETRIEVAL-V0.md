# AIOS Hybrid Retrieval V0

Phase 38 combines lexical and vector candidates using reciprocal-rank fusion (RRF).

```text
Query
  |
  +--> lexical candidates --+
  |                         |
  +--> vector candidates ---+--> RRF --> Top-K
```

## Why hybrid retrieval

Lexical search is strong for exact identifiers, names, error messages, and code symbols. Vector search is stronger for semantic similarity. Combining both gives AIOS a provider-neutral retrieval strategy without requiring a heavyweight reranker.

## RRF

Each candidate receives a rank-based contribution `1 / (60 + rank)` from each retrieval list. Candidate contributions are summed and the highest fused scores are returned.

## V0 boundaries

The phase does not introduce a neural reranker. It provides deterministic candidate fusion first. A later reranking layer can consume the fused candidate set and apply a model-based relevance score.

If no vector backend is configured, the system safely degrades to lexical retrieval.
