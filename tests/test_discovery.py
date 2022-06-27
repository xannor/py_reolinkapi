""" Discovery Tests """

from __future__ import annotations
import asyncio
import logging
import os
from struct import pack
from pytest import LogCaptureFixture, mark


from reolinkapi.discovery import PING_MESSAGE, PORT, Protocol
from reolinkapi.models.discovery import Device
from reolinkapi.typings.discovery import Device as DeviceType

TEST_MAC = 0xFFFFFFFFFFFF.to_bytes(6, 'big')
TEST_IDENT = "IPC"
TEST_IP = "255.255.255.255"
TEST_NAME = "Camera 1"
TEST_UUID = "QTZTIE1244023231"

class TestProtocol(Protocol):
    """Test Protocol"""

    def __init__(self, ping_message: bytes = PING_MESSAGE) -> None:
        super().__init__(ping_message)
        self._response:Device = None

    @property
    def response(self):
        """Response"""
        return self._response

    def discovered_device(self, device: Device) -> None:
        self._response = device
        logging.info("got %s", device)

def test_packet():
    """Test expected packet structure decoding"""

    proto = TestProtocol()
    proto.datagram_received(
        pack(
            "!50xQ18s4x6s18x4s16s4xL32s18s46x16s144x",
            0, #(Q) flags
            TEST_IDENT.encode("ascii"), #(20s) indentifier?
            TEST_MAC, # (6s) binary mac
            PING_MESSAGE, # (4s) message id
            TEST_IP.encode("ascii"), # (16s) IP string
            0x28230000,
            TEST_NAME.encode("ascii"), # (32s) name
            TEST_MAC.hex(":").encode("ascii"), # (18s) MAC string
            TEST_UUID.encode("ascii")
        ),
        ("localhost", PORT)
    )
    message = proto.response
    assert message is not None
    assert message.ident == TEST_IDENT
    assert message.ip == TEST_IP
    assert message.mac == TEST_MAC.hex(':')
    assert message.uuid == TEST_UUID

#@mark.skip("Manual run only")
async def test_live(caplog:LogCaptureFixture):
    """ Test Live Broadcast Ping and reply """
    caplog.set_level(logging.DEBUG)
    (transport, _) = await TestProtocol.listen()

    if broadcast := os.environ.get("DEV_PING", None):
        TestProtocol.ping(broadcast)
    else:
        TestProtocol.ping()
    await asyncio.sleep(4)
    transport.close()
    
    assert False
    