from aios.memory.store import MemoryStore


def test_memory_store_remember_and_search() -> None:
    store = MemoryStore()
    record = store.remember("AIOS uses a provider-neutral model gateway", source="test")
    assert record.source == "test"
    hits = store.search_text("model gateway")
    assert hits == [record]


def test_memory_store_namespace_isolation() -> None:
    store = MemoryStore()
    store.remember("private note", source="test", namespace="agent-a")
    assert store.search_text("private", namespace="agent-b") == []
