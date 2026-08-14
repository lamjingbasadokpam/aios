from aios.runtime.idempotency import EffectRegistry, EffectStatus


def test_duplicate_begin_returns_existing_effect() -> None:
    registry = EffectRegistry()
    first = registry.begin("run-1:tool-1")
    second = registry.begin("run-1:tool-1")
    assert first == second
    assert second.status == EffectStatus.IN_FLIGHT


def test_committed_effect_can_be_reused_without_reexecution() -> None:
    registry = EffectRegistry()
    registry.begin("run-1:tool-1")
    committed = registry.commit("run-1:tool-1", {"ok": True})
    assert registry.begin("run-1:tool-1") == committed
    assert registry.get("run-1:tool-1").result == {"ok": True}
