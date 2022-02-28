""" test auth mixin """

import logging
import os
from reolinkapi.rest.system import (
    System,
    AbilityRequest,
    AbilityResponse,
    DeviceInfoRequest,
    DeviceInfoResponse,
)

from reolinkapi.rest import Client
from .common import MockConnection

_JSON = {
    AbilityRequest: '[{"param": {"User": {"userName": null}}, "cmd": "GetAbility", "action": 0}]',
    AbilityResponse: '[{"cmd": "GetAbility", "code": 0, "value":null}]',
    DeviceInfoRequest: '[{"cmd": "DevInfo", "action": 0}]',
    DeviceInfoResponse: '[{"cmd": "DevInfo", "code": 0, "value": null}]',
}


class SystemTestRig(MockConnection, System):
    """System test rig"""

    JSON = _JSON


async def test_ability():
    """ability expected values test"""

    client = SystemTestRig()
    assert await client.get_ability()


async def test_live_ability(caplog):
    """login live test"""

    caplog.set_level(logging.DEBUG)
    client = Client()
    await client.connect(os.environ.get("DEV_IP", "localhost"))
    assert await client.login(
        os.environ.get("DEV_USER", "admin"), os.environ.get("DEV_PASS", "")
    )
    assert await client.get_ability()
    await client.disconnect()


async def test_devinfo():
    """device info test"""

    client = SystemTestRig()
    info = await client.get_device_info()
    assert info


async def test_live_devinfo(caplog):
    """device info live test"""

    caplog.set_level(logging.DEBUG)
    client = Client()
    await client.connect(os.environ.get("DEV_IP", "localhost"))
    assert await client.login(
        os.environ.get("DEV_USER", "admin"), os.environ.get("DEV_PASS", "")
    )
    info = await client.get_device_info()
    assert info
    await client.disconnect()
