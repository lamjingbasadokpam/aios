"""Local IPC transport reference using Unix domain sockets where supported."""

from __future__ import annotations

import asyncio
import json
from collections.abc import Awaitable, Callable
from pathlib import Path

from .contracts import MessageEnvelope, TransportKind


class IPCTransport:
    def __init__(self, socket_path: str | Path) -> None:
        self.socket_path = Path(socket_path)
        self._handler: Callable[[MessageEnvelope], Awaitable[MessageEnvelope | None]] | None = None

    def register_handler(self, handler: Callable[[MessageEnvelope], Awaitable[MessageEnvelope | None]]) -> None:
        self._handler = handler

    async def start(self) -> None:
        if self.socket_path.exists():
            self.socket_path.unlink()
        server = await asyncio.start_unix_server(self._handle, path=str(self.socket_path))
        async with server:
            await server.serve_forever()

    async def _handle(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            raw = await reader.readline()
            data = json.loads(raw.decode("utf-8"))
            message = MessageEnvelope.from_dict(data)
            response = await self._handler(message) if self._handler else None
            if response is not None:
                writer.write((json.dumps(response.to_dict()) + "\n").encode("utf-8"))
                await writer.drain()
        finally:
            writer.close()
            await writer.wait_closed()
