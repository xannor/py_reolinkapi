""" discovery helper """
from __future__ import annotations

import asyncio
import logging
from struct import pack
from typing import Any

_LOGGER = logging.getLogger(__name__);

PORT=2000
LISTEN=3000

PING_MESSAGE = pack("!L", 0xaaaa0000)

class BroadcastProtocol(asyncio.DatagramProtocol):
    """UDP Broadcast Protocal for device discovery"""

    def __init__(self, address:str = "255.255.255.255", port:int = PORT) -> None:
        self._address = address
        self._port = port
        self._transport: asyncio.DatagramTransport|None = None

    def connection_made(self, transport: asyncio.transports.DatagramTransport) -> None:
        self._transport = transport
        self.broadcast_ping()

    def connection_lost(self, exc: Exception | None) -> None:
        _LOGGER.debug("Closing Broadcast")
        self._transport = None

    def broadcast_ping(self) -> None:
        if self._transport is None:
            return
        self._transport.sendto(PING_MESSAGE, (self._address, self._port))

    def datagram_received(self, data: bytes, addr: tuple[str | Any, int]) -> None:
        _LOGGER.debug(f"B: Received data {data!r} from IP address {addr}")

    def error_received(self, exc: Exception) -> None:
        _LOGGER.debug(f"B: Received error {exc}")


class ReplyProtocol(asyncio.DatagramProtocol):
    """UDP Reply protocol for device discovery"""

    def __init__(self, port:int = LISTEN) -> None:
        self._port = port
        self._transport: asyncio.DatagramTransport|None = None

    def connection_made(self, transport: asyncio.transports.DatagramTransport) -> None:
        self._transport = transport

    def connection_lost(self, exc: Exception | None) -> None:
        _LOGGER("Closing listener")
        self._transport = None

    def datagram_received(self, data: bytes, addr: tuple[str | Any, int]) -> None:
        _LOGGER.debug(f"L: Received data {data!r} from IP address {addr}")
