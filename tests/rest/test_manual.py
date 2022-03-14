"""Manual tests for discovery and probing (do not run automated)"""

import logging
import os

from reolinkapi.rest import Client
from reolinkapi.typings.led import LightStates


async def test_manual(caplog):
    """manual code test"""

    caplog.set_level(logging.DEBUG)
    client = Client()
    await client.connect(os.environ.get("DEV_IP", "localhost"))
    assert await client.login(
        os.environ.get("DEV_USER", "admin"), os.environ.get("DEV_PASS", "")
    )
    commands = []
    commands.append(client.create_set_ir_lights(1, LightStates.OFF))
    commands.append(client.create_get_ir_lights(1))
    results = await client.batch(commands)

    await client.disconnect()
    assert False
