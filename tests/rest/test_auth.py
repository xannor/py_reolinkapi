""" test auth mixin """

import asyncio
import os
from reolinkapi.rest.auth import (
    Authentication,
    LoginRequest,
    LoginResponse,
)

from reolinkapi.rest import Client
from .common import MockConnection

_JSON = {
    LoginRequest: '[{"param": {"User": {"password": "", "userName": "admin"}}, "cmd": "Login", "action": 0}]',
    LoginResponse: '[{"cmd": "Login", "code": 0, "value":{"Token":{"leaseTime":0,"name":""}}}]',
}


class AuthTestRig(MockConnection, Authentication):
    """Auth test rig"""

    JSON = _JSON


async def test_login():
    """login expected values test"""

    client = AuthTestRig()
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
