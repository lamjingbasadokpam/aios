from aios.runtime.effect_boundary import EffectExecutionBoundary
from aios.runtime.effect_identity import EffectIntent
from aios.runtime.idempotency import EffectRegistry


def test_boundary_derives_key_from_effect_intent() -> None:
    calls = []
    boundary = EffectExecutionBoundary(EffectRegistry())
    intent = EffectIntent("run-1", "step-1", "send_email", {"to": "a@example.com"})

    first = boundary.execute(intent, lambda: calls.append("sent") or "ok")
    second = boundary.execute(intent, lambda: calls.append("sent") or "again")

    assert first.executed is True
    assert second.executed is False
    assert second.result == "ok"
    assert first.key == intent.key()
    assert calls == ["sent"]
