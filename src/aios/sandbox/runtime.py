"""Reference sandbox boundary for filesystem access."""

from __future__ import annotations

from pathlib import Path

from .contracts import SandboxSpec


class SandboxRuntime:
    def __init__(self, spec: SandboxSpec) -> None:
        self.spec = spec
        self.spec.workspace.mkdir(parents=True, exist_ok=True)

    def read_text(self, path: str) -> str:
        target = Path(path)
        if not self.spec.can_read(target):
            raise PermissionError(f"Sandbox read denied: {target}")
        return target.read_text(encoding="utf-8")

    def write_text(self, path: str, content: str) -> None:
        target = Path(path)
        if not self.spec.can_write(target):
            raise PermissionError(f"Sandbox write denied: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        encoded = content.encode("utf-8")
        if len(encoded) > self.spec.limits.max_output_bytes:
            raise ValueError("Sandbox output limit exceeded")
        target.write_text(content, encoding="utf-8")
