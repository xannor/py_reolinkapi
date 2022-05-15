from __future__ import annotations
import asyncio
import logging
from socket import AF_INET

from reolinkapi.discovery import BroadcastProtocol, ReplyProtocol

async def test_live(caplog):

    caplog.set_level(logging.DEBUG)
    loop = asyncio.get_event_loop()
    (ltransport, listener) = await loop.create_datagram_endpoint(lambda: ReplyProtocol(), family=AF_INET)
    (btransport, broadcast) = await loop.create_datagram_endpoint(lambda: BroadcastProtocol(), family=AF_INET, allow_broadcast=True)

    await asyncio.sleep(10)
    btransport.close()
    ltransport.close()
    
    assert False
    