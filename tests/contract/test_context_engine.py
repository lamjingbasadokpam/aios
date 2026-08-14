from aios.memory.context import ContextEngine
from aios.memory.contracts import MemoryHit, MemoryRecord


def test_context_engine_deduplicates_and_respects_budget() -> None:
    hits = [
        MemoryHit(MemoryRecord("important AIOS architecture", "doc"), 0.9),
        MemoryHit(MemoryRecord("important AIOS architecture", "other"), 0.8),
        MemoryHit(MemoryRecord("second fact", "doc"), 0.7),
    ]
    pack = ContextEngine(max_tokens=6).pack(hits)
    assert len(pack.items) == 1
    assert pack.items[0].source == "doc"
    assert pack.truncated is True


def test_context_engine_preserves_provenance_metadata() -> None:
    record = MemoryRecord("source-backed fact", "manual.md", metadata={"page": 4})
    pack = ContextEngine(max_tokens=20).pack([MemoryHit(record, 1.0)])
    assert pack.items[0].source == "manual.md"
    assert pack.items[0].metadata["page"] == 4
