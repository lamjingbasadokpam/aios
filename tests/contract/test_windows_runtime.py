import os
from pathlib import Path

import pytest

from aios.runtime.named_pipe import NamedPipeEndpoint, WindowsNamedPipeTransport
from aios.runtime.process import WindowsProcessAdapter
from aios.runtime.windows import WindowsRuntime


def test_capabilities_report_current_platform() -> None:
    capabilities = WindowsRuntime().capabilities()
    assert capabilities.windows is (os.name == "nt")
    assert isinstance(capabilities.python, (str, type(None)))


def test_working_directory_validation(tmp_path: Path) -> None:
    assert WindowsRuntime.validate_working_directory(tmp_path) == tmp_path.resolve()
    with pytest.raises(NotADirectoryError):
        WindowsRuntime.validate_working_directory(tmp_path / "missing")


def test_command_builder() -> None:
    assert WindowsRuntime.command("python", "-V") == ["python", "-V"]


def test_named_pipe_endpoint() -> None:
    endpoint = NamedPipeEndpoint("aios-agent-test")
    assert endpoint.address == r"\\.\pipe\aios-agent-test"
    assert WindowsNamedPipeTransport(endpoint).address() == endpoint.address


def test_process_adapter_is_windows_only() -> None:
    if os.name != "nt":
        with pytest.raises(OSError):
            WindowsProcessAdapter().spawn(["python", "-c", "print(1)"], cwd=".")
