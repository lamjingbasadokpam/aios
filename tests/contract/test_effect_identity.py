from aios.runtime.effect_identity import EffectIntent


def test_equivalent_intents_have_same_key() -> None:
    a = EffectIntent("run-1", "step-2", "send_email", {"to": "a@example.com", "subject": "Hi"})
    b = EffectIntent("run-1", "step-2", "send_email", {"subject": "Hi", "to": "a@example.com"})
    assert a.key() == b.key()


def test_different_effect_version_changes_key() -> None:
    a = EffectIntent("run-1", "step-2", "tool", {"x": 1}, "v1")
    b = EffectIntent("run-1", "step-2", "tool", {"x": 1}, "v2")
    assert a.key() != b.key()
