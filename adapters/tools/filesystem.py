"""Bounded filesystem tools.

The handler never accepts an arbitrary path without checking it against the
configured workspace root. This is deliberately narrower than a general shell
or filesystem API.
"""

from __future__ import annotations

from pathlib import Path

from aios.tools.contracts import Tool, ToolContext, ToolResult


FILESYSTEM_READ = "filesystem.read"
FILESYSTEM_WRITE = "filesystem.write"


def _safe_path(root: Path, requested: str) -> Path:
    root = root.resolve()
    candidate = (root / requested).resolve()
    if candidate != root and root not in candidate.parents:
        raise PermissionError("Path escapes the AIOS workspace")
    return candidate


def read_tool(workspace: Path) -> tuple[Tool, object]:
    async def handler(arguments: dict, context: ToolContext) -> ToolResult:
        try:
            path = _safe_path(workspace, str(arguments["path"]))
        except PermissionError:
            raise
        try:
            text = path.read_text(encoding="utf-8")
            return ToolResult(success=True, output=text, tool_id="filesystem.read")
        except Exception as exc:
            return ToolResult(success=False, error=str(exc), tool_id="filesystem.read")

    return Tool(
        tool_id="filesystem.read",
        name="read_file",
        description="Read a UTF-8 text file inside the AIOS workspace.",
        input_schema={"type": "object", "required": ["path"]},
        required_capabilities=frozenset({FILESYSTEM_READ}),
        risk_level="low",
        filesystem_required=True,
    ), handler


def write_tool(workspace: Path) -> tuple[Tool, object]:
    async def handler(arguments: dict, context: ToolContext) -> ToolResult:
        try:
            path = _safe_path(workspace, str(arguments["path"]))
        except PermissionError:
            raise
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(str(arguments.get("content", "")), encoding="utf-8")
            return ToolResult(success=True, output=str(path.relative_to(workspace)), tool_id="filesystem.write")
        except Exception as exc:
            return ToolResult(success=False, error=str(exc), tool_id="filesystem.write")

    return Tool(
        tool_id="filesystem.write",
        name="write_file",
        description="Write a UTF-8 text file inside the AIOS workspace.",
        input_schema={"type": "object", "required": ["path", "content"]},
        required_capabilities=frozenset({FILESYSTEM_WRITE}),
        risk_level="medium",
        filesystem_required=True,
    ), handler
