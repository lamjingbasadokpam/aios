import os

import pytest

from aios.runtime.resources import ResourceLimits, WindowsJobObjectAdapter


def test_resource_limits_are_explicit() -> None:
    limits = ResourceLimits(max_processes=2, memory_bytes=1024, cpu_time_seconds=30)
    assert limits.max_processes == 2
    assert limits.memory_bytes == 1024
    assert limits.cpu_time_seconds == 30


def test_job_adapter_is_platform_gated() -> None:
    adapter = WindowsJobObjectAdapter(ResourceLimits(max_processes=1))
    assert adapter.supported is (os.name == "nt")
    if os.name != "nt":
        with pytest.raises(OSError):
            adapter.attach(1)
