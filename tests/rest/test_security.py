""" test auth mixin """

import os
from reolinkapi.rest.security import (
    Security,
    LoginRequest,
    LoginResponse,
)

from reolinkapi.rest import Client
from .common import MockConnection

_JSON = {
    LoginRequest: '[{"cmd": "Login", "action": 0, "param": {"User": {"userName": "admin", "password": ""}}}]',
    LoginResponse: '[{"cmd": "Login", "code": 0, "value":{"Token":{"leaseTime":0,"name":""}}}]',
}


class SecurityTestRig(MockConnection, Security):
    """Security test rig"""

    JSON = _JSON


async def test_login():
    """login expected values test"""

    client = SecurityTestRig()
    assert await client.login()


async def test_live_fail_login():
    """login live test (admin-empty = expect failure)"""

    client = Client()
    await client.connect("westside-cam.home.botf.co")
    assert not await client.login()


async def test_live_login():
    """login live test"""

    client = Client()
    await client.connect(os.environ.get("DEV_IP", "localhost"))
    assert await client.login(
        os.environ.get("DEV_USER", "admin"), os.environ.get("DEV_PASS", "")
    )
    await client.disconnect()
