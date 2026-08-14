"""Windows Named Pipe transport boundary for AIOS.

The transport is isolated from the gateway so Windows IPC details never leak
into agent or orchestration code. V0 exposes a safe endpoint contract and
availability check; byte-level pipe serving belongs to the Windows host
adapter once the supported Python/runtime API is selected.
"""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NamedPipeEndpoint:
    name: str

    def __post_init__(self) -> None:
        if not self.name or "\\" in self.name.replace("\\\\.\\pipe\\", ""):
            raise ValueError("Invalid Named Pipe name")

    @property
    def address(self) -> str:
        return f"\\\\.\\pipe\\{self.name}"


class WindowsNamedPipeTransport:
    def __init__(self, endpoint: NamedPipeEndpoint) -> None:
        self.endpoint = endpoint

    @staticmethod
    def supported() -> bool:
        return os.name == "nt"

    def address(self) -> str:
        return self.endpoint.address
