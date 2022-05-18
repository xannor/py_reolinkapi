""" discovery helper """
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
import logging
import socket
from struct import pack
from typing import Any, Callable

_LOGGER = logging.getLogger(__name__)

PORT=3000
PING=2000

# the cameras expect this value and reply with it as a checksum
PING_MESSAGE = pack("!L", 0xaaaa0000)

@dataclass
class DiscoveryMessage:
    """Discovery Response Message"""

    ip: str
    mac: str
    name: str
    ident: str|None = field(default=None)
    uuid: str|None = field(default=None)

DISCOVERY_CALLBACK = Callable[[DiscoveryMessage], None]

def _nulltermstring(value:bytes, offset:int, maxlength:int = None)->str|None:
    idx = value.index(0, offset);
    if idx <= offset:
        return None
    if maxlength is not None and offset - idx > maxlength:
        idx = offset + maxlength
    return value[offset:idx].decode("ascii")

class DiscoveryProtocol(asyncio.DatagramProtocol):
    """UDP Discovery Protocol"""

    def __init__(self, discovery: DISCOVERY_CALLBACK, ping_message:bytes = PING_MESSAGE) -> None:
        self._transport:asyncio.transports.DatagramTransport = None
        self._ondiscovered = discovery
        self._reply_verify = ping_message

    def connection_made(self, transport: asyncio.transports.DatagramTransport) -> None:
        self._transport = transport
        _LOGGER.debug("Listener connected %s", transport.get_extra_info("sockname"))

    def connection_lost(self, exc: Exception | None) -> None:
        if exc is not None:
            _LOGGER.error("Listener received error")
        self._transport = None
        _LOGGER.debug("Listener disconnected")

    def datagram_received(self, data: bytes, addr: tuple[str | Any, int]) -> None:
        if len(data) != 388:
            return

        # offsets
        # 50+8   - flags?
        # 58+20  - zero padded identifier string? Lumus (only?) sends "IPC" here
        # 80+6   - binary MAC
        # 104+4  - replay of ping message? need to confirm if it is a repeat or always the "original"
        # 108+16 - zero padded ip string +4, not sure if they went 20chars or if there is a 4 byte data point
        # 128+4  - another marker? consistently 0x28230000
        # 132+32 - zero padded name string
        # 164+18 - zero padded MAC string
        # 228+16 - zero padded UUID string, not sure how long this could be as there is a lot of padding

        if data[104:108] != self._reply_verify:
            return

        #_LOGGER.debug(
        #    "%r; %r; %r; %r; %r; %r; %r", 
        #    data[50:58], 
        #    data[128:132], 
        #    data[0:50].strip(b'\0').rstrip(b'\0'),
        #    data[62:80].strip(b'\0').rstrip(b'\0'),
        #    data[86:104].strip(b'\0').rstrip(b'\0'),
        #    data[148:164].strip(b'\0').rstrip(b'\0'),
        #    data[244:].strip(b'\0').rstrip(b'\0'),
        #)

        message = DiscoveryMessage(
            _nulltermstring(data, 108, 20),
            _nulltermstring(data,164,18) or data[80:86].hex(':').upper(),
            _nulltermstring(data, 132, 32),
            _nulltermstring(data,58,20),
            _nulltermstring(data,228,32)
        )

        self._ondiscovered(message)
        

async def async_start(discovery:DISCOVERY_CALLBACK, *, address:str="0.0.0.0", port:int = PORT):
    """ setup listener """
    loop = asyncio.get_event_loop()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setblocking(False)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((address, port))
    (transport, _) = await loop.create_datagram_endpoint(lambda: DiscoveryProtocol(discovery), sock=sock)
    
    def close():
        transport.close()

    return close

def async_ping(*, address:str = "255.255.255.255", port: int = PING, payload:bytes = PING_MESSAGE):
    """Send device ping to network"""

    _LOGGER.debug("P: pinging %s:%s", address, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(payload, (address, port))
