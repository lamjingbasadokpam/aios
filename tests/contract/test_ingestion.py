from aios.memory.ingestion import Document, TextChunker, chunks_to_records


def test_chunker_preserves_provenance_and_overlap() -> None:
    document = Document("one two three four five six seven eight", "notes.md", "doc-1", {"type": "markdown"})
    chunks = TextChunker(max_chars=15, overlap=3).chunk(document)
    assert len(chunks) > 1
    assert all(chunk.document_id == "doc-1" for chunk in chunks)
    assert chunks[0].source == "notes.md"
    records = chunks_to_records(chunks, namespace="agent-a")
    assert records[0].namespace == "agent-a"
    assert records[0].metadata["document_id"] == "doc-1"
    assert records[0].metadata["chunk_index"] == 0


def test_empty_document_produces_no_chunks() -> None:
    document = Document("   ", "empty.txt", "doc-2", {})
    assert TextChunker().chunk(document) == []
