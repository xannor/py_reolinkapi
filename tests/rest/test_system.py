""" test auth mixin """

import logging
import os
from reolinkapi.rest.system import (
    System,
    GET_ABILITY_COMMAND,
    DEVICE_INFO_COMMAND,
)

from reolinkapi.rest import Client
from .common import MockConnection

_JSON = {
    GET_ABILITY_COMMAND: (
        '[{"cmd": "GetAbility", "action": 0, "param": {"User": {"userName": "null"}}}]',
        '[{"cmd": "GetAbility", "code": 0, "value":{"Ability":{}}}]',
    ),
    DEVICE_INFO_COMMAND: (
        '[{"cmd": "GetDevInfo", "action": 0}]',
        '[{"cmd": "GetDevInfo", "code": 0, "value": {"DevInfo":{}}}]',
    ),
}


class SystemTestRig(MockConnection, System):
    """System test rig"""

    JSON = _JSON


async def test_ability():
    """ability expected values test"""

    client = SystemTestRig()
    assert await client.get_ability() is not None


async def test_live_ability(caplog):
    """login live test"""

    caplog.set_level(logging.DEBUG)
    client = Client()
    await client.connect(os.environ.get("DEV_IP", "localhost"))
    assert await client.login(
        os.environ.get("DEV_USER", "admin"), os.environ.get("DEV_PASS", "")
    )
    abilities = await client.get_ability()
    await client.disconnect()
    assert abilities


async def test_devinfo():
    """device info test"""

    client = SystemTestRig()
    info = await client.get_device_info()
    assert info is not None


async def test_live_devinfo(caplog):
    """device info live test"""

    caplog.set_level(logging.DEBUG)
    client = Client()
    await client.connect(os.environ.get("DEV_IP", "localhost"))
    assert await client.login(
        os.environ.get("DEV_USER", "admin"), os.environ.get("DEV_PASS", "")
    )
    info = await client.get_device_info()
    assert info is not None
    await client.disconnect()
