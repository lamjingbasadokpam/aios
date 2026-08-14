import asyncio
from pathlib import Path
import sys

import pytest

from aios.execution import ExecutionDenied, ExecutionRequest, ProcessExecutor


def test_allowlisted_process_runs_inside_workspace(tmp_path: Path) -> None:
    executor = ProcessExecutor(frozenset({sys.executable}), tmp_path)
    request = ExecutionRequest(
        executable=sys.executable,
        arguments=("-c", "print('aios')"),
    )
    result = asyncio.run(executor.run(request))
    assert result.success
    assert result.exit_code == 0
    assert "aios" in result.stdout


def test_non_allowlisted_executable_is_denied(tmp_path: Path) -> None:
    executor = ProcessExecutor(frozenset(), tmp_path)
    with pytest.raises(ExecutionDenied):
        asyncio.run(executor.run(ExecutionRequest(executable=sys.executable)))


def test_working_directory_cannot_escape(tmp_path: Path) -> None:
    executor = ProcessExecutor(frozenset({sys.executable}), tmp_path)
    with pytest.raises(ExecutionDenied):
        asyncio.run(executor.run(ExecutionRequest(executable=sys.executable, working_directory="..")))
