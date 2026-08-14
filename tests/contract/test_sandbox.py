from pathlib import Path

import pytest

from aios.sandbox import ResourceLimits, SandboxRuntime, SandboxSpec


def test_sandbox_scopes_reads_and_writes(tmp_path: Path) -> None:
    workspace = tmp_path / "workspace"
    allowed = tmp_path / "allowed"
    denied = tmp_path / "denied"
    allowed.mkdir()
    denied.mkdir()
    (allowed / "input.txt").write_text("ok", encoding="utf-8")
    (denied / "secret.txt").write_text("no", encoding="utf-8")
    runtime = SandboxRuntime(SandboxSpec(workspace, read_paths=(allowed,), write_paths=(workspace,)))
    assert runtime.read_text(str(allowed / "input.txt")) == "ok"
    with pytest.raises(PermissionError):
        runtime.read_text(str(denied / "secret.txt"))
    runtime.write_text(str(workspace / "out.txt"), "result")


def test_sandbox_enforces_output_limit(tmp_path: Path) -> None:
    runtime = SandboxRuntime(SandboxSpec(tmp_path, write_paths=(tmp_path,), limits=ResourceLimits(max_output_bytes=3)))
    with pytest.raises(ValueError):
        runtime.write_text(str(tmp_path / "large.txt"), "1234")
