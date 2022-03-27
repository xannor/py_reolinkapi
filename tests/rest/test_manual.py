"""Manual tests for discovery and probing (do not run automated)"""

import logging
import os
from reolinkapi.const import DEFAULT_PASSWORD, DEFAULT_USERNAME

from reolinkapi.rest import Client


async def test_manual(caplog):
    """manual code test"""

    caplog.set_level(logging.DEBUG)


async def test_manual_live(caplog):
    """manual code test (live)"""

    caplog.set_level(logging.DEBUG)
    client = Client()
    await client.connect(os.environ.get("DEV_IP", "localhost"))
    assert await client.login(
        os.environ.get("DEV_USER", DEFAULT_USERNAME),
        os.environ.get("DEV_PASS", DEFAULT_PASSWORD),
    )
    result = await client.search()

    await client.disconnect()

    assert False
