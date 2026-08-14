import os
from pathlib import Path

import pytest

from aios.runtime.windows import WindowsRuntime


def test_capabilities_report_current_platform() -> None:
    capabilities = WindowsRuntime().capabilities()
    assert capabilities.windows is (os.name == "nt")


def test_working_directory_validation(tmp_path: Path) -> None:
    assert WindowsRuntime.validate_working_directory(tmp_path) == tmp_path.resolve()
    with pytest.raises(NotADirectoryError):
        WindowsRuntime.validate_working_directory(tmp_path / "missing")


def test_command_builder() -> None:
    assert WindowsRuntime.command("python", "-V") == ["python", "-V"]
