""" Discovery Tests """

from __future__ import annotations
import asyncio
import logging
from socket import AF_INET
from pytest import LogCaptureFixture

from reolinkapi.discovery import async_start, async_ping

async def test_live(caplog:LogCaptureFixture):
    """ Test Live Broadcast Ping and reply """
    caplog.set_level(logging.DEBUG)
    shutdown = await async_start(lambda d: logging.info("got %s", d))

    async_ping()
    await asyncio.sleep(4)
    shutdown()
    
    assert False
    