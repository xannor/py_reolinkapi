""" test auth mixin """

import logging
import os
from reolinkapi.rest.security import Security
from reolinkapi.helpers.security import LOGIN_COMMAND, LOGOUT_COMMAND


from reolinkapi.rest import Client
from .common import MockConnection

_JSON = {
    LOGIN_COMMAND: (
        '[{"cmd": "Login", "action": 0, "param": {"User": {"userName": "admin", "password": ""}}}]',
        '[{"cmd": "Login", "code": 0, "value":{"Token":{"leaseTime":0,"name":""}}}]',
    ),
    LOGOUT_COMMAND: (
        '[{"cmd": "Logout", "action": 0}]',
        '[{"cmd": "Logout", "code": 0}]',
    ),
}


class SecurityTestRig(MockConnection, Security):
    """Security test rig"""

    JSON = _JSON


async def test_login():
    """login expected values test"""

    client = SecurityTestRig()
    assert await client.login()


async def test_live_fail_login(caplog):
    """login live test (admin-empty = expect failure)"""

    caplog.set_level(logging.DEBUG)
    client = Client()
    await client.connect(os.environ.get("DEV_IP", "localhost"))
    assert not await client.login()


async def test_live_login(caplog):
    """login live test"""

    caplog.set_level(logging.DEBUG)
    client = Client()
    await client.connect(os.environ.get("DEV_IP", "localhost"))
    assert await client.login(
        os.environ.get("DEV_USER", "admin"), os.environ.get("DEV_PASS", "")
    )
    await client.disconnect()
