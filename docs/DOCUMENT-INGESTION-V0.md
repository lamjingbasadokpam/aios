# AIOS Document Ingestion and Chunking V0

Phase 37 turns source documents into provenance-aware memory records suitable for indexing.

```text
Source
  |
  v
Document
  |
  v
TextChunker
  |
  +--> Chunk 0
  +--> Chunk 1
  +--> Chunk N
          |
          v
MemoryRecord
          |
          v
Embedding / VectorIndex
```

## V0 scope

- Provider-neutral `Document` representation.
- Injectable `DocumentLoader` contract for future Markdown, PDF, code, web and connector loaders.
- Character-bounded chunking with configurable overlap.
- Source/document/chunk provenance preserved in metadata.
- Conversion into existing `MemoryRecord` and namespace contracts.

## Design rule

Ingestion does not embed, rank, or retrieve. It only normalizes source material into chunks. This keeps extraction, chunking, indexing, and retrieval independently replaceable.

## Next evolution

Future phases can add real loaders, token-aware chunking, structure-aware Markdown/code splitting, deduplication, incremental indexing, and content hashing.
