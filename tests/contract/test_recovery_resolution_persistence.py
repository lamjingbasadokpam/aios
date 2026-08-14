from aios.runtime.recovery_resolution_persistence import RecoveryResolutionRecord, RecoveryResolutionStore


def test_resolution_is_persisted_as_structured_event() -> None:
    seen = []
    store = RecoveryResolutionStore(lambda event_type, payload: seen.append((event_type, payload)))
    record = RecoveryResolutionRecord("e1", "confirmed", 7)
    store.persist(record)
    assert seen == [("recovery_resolution", {"effect_key": "e1", "resolution": "confirmed", "sequence": 7})]


def test_replay_keeps_latest_resolution_per_effect() -> None:
    records = [
        RecoveryResolutionRecord("e1", "pending", 1),
        RecoveryResolutionRecord("e2", "confirmed", 2),
        RecoveryResolutionRecord("e1", "confirmed", 3),
        RecoveryResolutionRecord("e1", "stale", 2),
    ]
    latest = RecoveryResolutionStore.replay(records)
    assert latest["e1"].resolution == "confirmed"
    assert latest["e1"].sequence == 3
    assert latest["e2"].resolution == "confirmed"
