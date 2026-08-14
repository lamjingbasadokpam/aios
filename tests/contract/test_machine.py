from pathlib import Path

import pytest

from aios.machine import Capability, CapabilityRequest, Decision, LocalMachineRuntime
from aios.machine.contracts import Policy


def test_machine_runtime_allows_explicit_capability(tmp_path: Path) -> None:
    target = tmp_path / "note.txt"
    target.write_text("hello", encoding="utf-8")
    runtime = LocalMachineRuntime(Policy(allowed=frozenset({Capability.FILE_READ})))
    assert runtime.read_text(str(target), "agent") == "hello"


def test_machine_runtime_denies_by_default(tmp_path: Path) -> None:
    target = tmp_path / "note.txt"
    target.write_text("secret", encoding="utf-8")
    runtime = LocalMachineRuntime()
    with pytest.raises(PermissionError):
        runtime.read_text(str(target), "agent")


def test_approval_required_can_be_approved() -> None:
    runtime = LocalMachineRuntime(Policy(approval_required=frozenset({Capability.NETWORK})))
    request = CapabilityRequest(Capability.NETWORK, "example.com", "agent")
    runtime.set_approval_handler(lambda _: True)
    assert runtime.authorize(request) == Decision.ALLOW
