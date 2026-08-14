from aios.runtime.effect_boundary import EffectExecutionBoundary
from aios.runtime.idempotency import EffectRegistry


def test_committed_effect_is_not_executed_twice() -> None:
    calls = []
    boundary = EffectExecutionBoundary(EffectRegistry())

    def operation():
        calls.append(1)
        return "ok"

    first = boundary.execute("effect-1", operation)
    second = boundary.execute("effect-1", operation)

    assert first.executed is True
    assert second.executed is False
    assert second.result == "ok"
    assert len(calls) == 1
