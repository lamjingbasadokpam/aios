# AIOS Context Engine V0

Phase 39 turns retrieval results into bounded model context.

```text
Retrieved hits
     |
     v
Context Engine
     |
     +--> sort by relevance
     +--> deduplicate
     +--> preserve provenance
     +--> enforce token budget
     |
     v
ContextPack
```

## Contract

`ContextEngine.pack()` produces a `ContextPack` containing the selected items, an estimated token count, and whether the budget caused truncation.

V0 estimates tokens conservatively from characters (`ceil(chars / 4)`) rather than depending on a provider-specific tokenizer.

## Design rules

- Retrieved content must not bypass the context budget.
- Duplicate content is removed before packing.
- Source and metadata remain attached to every context item.
- Model-provider tokenizers are an adapter concern and can replace the estimate later.
- Context packing is separate from retrieval so orchestration can reuse it for memory, tool observations, and future system context.
