""" test auth mixin """

import logging
import os
from reolinkapi.base.led import LED
from reolinkapi.helpers.led import (
    GET_IR_LIGHTS_COMMAND,
    SET_IR_LIGHTS_COMMAND,
    GET_POWER_LED_COMMAND,
    SET_POWER_LED_COMMAND,
    GET_WHITE_LED_COMMAND,
    SET_WHITE_LED_COMMAND,
)

from reolinkapi.rest import Client
from .common import MockConnection

_JSON = {
    GET_IR_LIGHTS_COMMAND: (
        '[{"cmd": "GetLocalLink", "action": 0}]',
        '[{"cmd": "GetLocalLink", "code": 0, "value":{}}]',
    ),
    SET_IR_LIGHTS_COMMAND: (
        '[{"cmd": "GetLocalLink", "action": 0}]',
        '[{"cmd": "GetLocalLink", "code": 0, "value":{}}]',
    ),
    GET_POWER_LED_COMMAND: (
        '[{"cmd": "GetChannelstatus", "action": 0}]',
        '[{"cmd": "GetChannelstatus", "code": 0, "value":{"status":[], "count": 0}}]',
    ),
    SET_POWER_LED_COMMAND: (
        '[{"cmd": "GetChannelstatus", "action": 0}]',
        '[{"cmd": "GetChannelstatus", "code": 0, "value":{"status":[], "count": 0}}]',
    ),
    GET_WHITE_LED_COMMAND: (
        '[{"cmd": "GetNetPort", "action": 0}]',
        '[{"cmd": "GetNetPort", "code": 0, "value":{}}]',
    ),
    SET_WHITE_LED_COMMAND: (
        '[{"cmd": "GetP2p", "action": 0}]',
        '[{"cmd": "GetP2p", "code": 0, "value":{"P2p":{}}}]',
    ),
}


class LEDTestRig(MockConnection, LED):
    """Led test rig"""

    JSON = _JSON


async def test_get_irlights():
    """get ir lights expected values test"""

    client = LEDTestRig()
    assert await client.get_ir_lights() is not None


async def test_live_get_irlights(caplog):
    """get ir lights live test"""

    caplog.set_level(logging.DEBUG)
    client = Client()
    await client.connect(os.environ.get("DEV_IP", "localhost"))
    assert await client.login(
        os.environ.get("DEV_USER", "admin"), os.environ.get("DEV_PASS", "")
    )
    info = await client.get_ir_lights()
    assert info is not None
    await client.disconnect()
