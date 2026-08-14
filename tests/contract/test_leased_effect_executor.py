from aios.runtime.effect_identity import EffectIntent
from aios.runtime.effect_lease import EffectLeaseStore
from aios.runtime.leased_effect_executor import LeasedEffectExecutor


def test_executor_commits_and_deduplicates() -> None:
    executor = LeasedEffectExecutor(EffectLeaseStore())
    intent = EffectIntent("run-1", "step-1", "tool", {"x": 1})
    calls = []

    first = executor.execute(intent, "worker-a", lambda: calls.append(1) or "ok")
    second = executor.execute(intent, "worker-a", lambda: calls.append(1) or "bad")

    assert first.executed is True
    assert second.executed is False
    assert second.result == "ok"
    assert len(calls) == 1


def test_other_worker_cannot_execute_live_lease() -> None:
    leases = EffectLeaseStore()
    executor = LeasedEffectExecutor(leases)
    intent = EffectIntent("run-2", "step-1", "tool", {"x": 1})
    executor.leases.claim(intent.key(), "worker-a")

    try:
        executor.execute(intent, "worker-b", lambda: "bad")
    except RuntimeError as exc:
        assert "owned by another worker" in str(exc)
    else:
        raise AssertionError("expected lease ownership failure")
