"""test encrypt mixin"""

import json
import logging
import os
from reolinkapi.rest import Client

from reolinkapi.rest.encrypt import Encrypt
from reolinkapi.typings.commands import CommandRequestWithParam
from reolinkapi.rest.security import LOGIN_COMMAND
from reolinkapi.const import DEFAULT_USERNAME, DEFAULT_PASSWORD

_JSON = {
    LOGIN_COMMAND: (
        '[{"cmd": "Login", "action": 0, "param": {"User": {"userName": "admin", "password": ""}}}]',
        '[{"cmd": "Login", "code": 0, "value":{"Token":{"leaseTime":0,"name":""}}}]',
    ),
}

_AUTH_HEADER = 'Digest qop="auth", realm="IPC",nonce=".....", stale="FALSE", nc="...."'


class MockClientResponse:
    """Mock aiohttp ClientResponse"""

    def __init__(self, url: str, headers: dict, text: str) -> None:
        self.url = lambda: None
        setattr(self.url, "path_qs", url)
        self.headers = headers
        self._text = text
        self.method = "POST"

    async def text(self):
        """text"""
        return self._text

    def close(self):
        """close"""


class EncryptTestRig(Encrypt):
    """Encryp mixin test rig"""

    async def _execute_request(
        self, *args: CommandRequestWithParam, use_get: bool = False
    ):  # pylint: disable=method-hidden
        _j = json.dumps(args)

        if args[0]["cmd"] == LOGIN_COMMAND and "Digest" not in args[0]["param"]:
            return (
                MockClientResponse(
                    "/cgi-bin/api.cgi?cmd=Login",
                    {"WWW-Authenticate": _AUTH_HEADER},
                    "",
                ),
                False,
            )
        return (
            MockClientResponse(
                "",
                {},
                "",
            ),
            True,
        )

    async def _process_response(
        self, response: MockClientResponse
    ):  # pylint: disable=method-hidden
        data = self._encrypt(_JSON[LOGIN_COMMAND][1])
        data = self._decrypt(data)
        data = json.loads(data)
        response.close()
        return data

    async def login(
        self, username: str = DEFAULT_USERNAME, password: str = DEFAULT_PASSWORD
    ):
        """Mock Login"""
        results = await self._encrypted_login(username, password)
        assert results is not None
        return True

    def create_cipher(self, key: str):
        """create cipher"""
        return self._create_cipher(key)

    def decrypt(self, data: str):
        """decrypt"""
        return self._decrypt(data)


async def test_login():
    """login expected values test"""

    # global _AUTH_HEADER
    # _AUTH_HEADER = os.environ.get("DEV_AUTH", _AUTH_HEADER)

    client = EncryptTestRig()
    assert await client.login(
        os.environ.get("DEV_USER", DEFAULT_USERNAME),
        os.environ.get("DEV_PASS", DEFAULT_PASSWORD),
    )


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


def test_aes_encoding():
    """manual decode test"""
    client = EncryptTestRig()
    client.create_cipher(os.environ.get("DEV_AES_KEY", ""))
    data = client.decrypt(os.environ.get("DEV_ENCODED"))
    assert data
