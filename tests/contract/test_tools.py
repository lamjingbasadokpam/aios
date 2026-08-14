import asyncio
from pathlib import Path

import pytest

from aios.tools import ToolContext, ToolGateway, ToolRegistry
from aios.tools.gateway import ToolDenied
from adapters.tools.filesystem import FILESYSTEM_READ, FILESYSTEM_WRITE, read_tool, write_tool


def make_gateway(tmp_path: Path) -> ToolGateway:
    registry = ToolRegistry()
    read, read_handler = read_tool(tmp_path)
    write, write_handler = write_tool(tmp_path)
    registry.register(read, read_handler)
    registry.register(write, write_handler)
    return ToolGateway(registry)


def test_filesystem_write_and_read_are_workspace_bounded(tmp_path: Path) -> None:
    gateway = make_gateway(tmp_path)
    write_context = ToolContext(granted_capabilities=frozenset({FILESYSTEM_WRITE}))
    read_context = ToolContext(granted_capabilities=frozenset({FILESYSTEM_READ}))

    result = asyncio.run(gateway.invoke("filesystem.write", {"path": "note.txt", "content": "hello"}, write_context))
    assert result.success

    result = asyncio.run(gateway.invoke("filesystem.read", {"path": "note.txt"}, read_context))
    assert result.output == "hello"

    with pytest.raises(PermissionError):
        asyncio.run(gateway.invoke("filesystem.read", {"path": "../outside.txt"}, read_context))


def test_missing_capability_denies_tool(tmp_path: Path) -> None:
    gateway = make_gateway(tmp_path)
    with pytest.raises(ToolDenied):
        asyncio.run(gateway.invoke("filesystem.write", {"path": "x.txt", "content": "x"}, ToolContext()))
