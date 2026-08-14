import pytest

from aios.runtime.effect_recovery_events import EffectRecoveryEvent, EffectRecoveryEventType
from aios.runtime.recovery_gate import RecoveryResumeGate
from aios.runtime.recovery_state import RecoveryStateRehydrator


def test_gate_allows_clean_recovery() -> None:
    state = RecoveryStateRehydrator().rehydrate([
        EffectRecoveryEvent(EffectRecoveryEventType.EFFECT_REUSED, "effect-1", "committed", "ok")
    ])
    decision = RecoveryResumeGate().evaluate(state)
    assert decision.allowed is True


def test_gate_blocks_reconciliation_required_state() -> None:
    state = RecoveryStateRehydrator().rehydrate([
        EffectRecoveryEvent(EffectRecoveryEventType.EFFECT_RECONCILIATION_REQUIRED, "effect-1", "lease expired")
    ])
    gate = RecoveryResumeGate()
    decision = gate.evaluate(state)
    assert decision.allowed is False
    with pytest.raises(RuntimeError, match="reconciliation"):
        gate.require_resume(state)
