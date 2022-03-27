"""test encrypt mixin"""
from __future__ import annotations

import json
import logging
import os
from reolinkapi.rest import Client

from reolinkapi.rest.encrypt import Encrypt
from reolinkapi.typings.commands import CommandRequestWithParam
from reolinkapi.helpers.security import LOGIN_COMMAND
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

    def __init__(self, *args, **kwargs):
        self.__auth_header = kwargs.pop("AUTH_HEADER", None)
        if self.__auth_header is None:
            self.__auth_header = _AUTH_HEADER
        self.__create_nonce = kwargs.pop("CNONCE", None)
        self.__cipher_key = ""
        self.__token_response = kwargs.pop("TOKEN", None)
        if self.__token_response is None:
            self.__token_response = _JSON[LOGIN_COMMAND][1]
        super().__init__(*args, **kwargs)

    def _create_nonce(self):
        if self.__create_nonce is not None:
            return self.__create_nonce()
        return super()._create_nonce()

    async def _execute_request(
        self, *args: CommandRequestWithParam, use_get: bool = False
    ):  # pylint: disable=method-hidden
        _j = json.dumps(args)

        if args[0]["cmd"] == LOGIN_COMMAND and "Digest" not in args[0]["param"]:
            return MockClientResponse(
                "/cgi-bin/api.cgi?cmd=Login",
                {"WWW-Authenticate": self.__auth_header},
                "",
            )
        return MockClientResponse(
            "/cgi-bin/api.cgi?cmd=Login",
            {},
            self._encrypt(self.__token_response)
            if self.__token_response[0] == "["
            else self.__token_response,
        )

    async def _process_response(
        self, response: MockClientResponse
    ):  # pylint: disable=method-hidden
        data = self._decrypt(await response.text())
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

    def _create_cipher(self, key: str):
        self.__cipher_key = key
        return super()._create_cipher(key)

    @property
    def cipher_key(self):
        """get cipher key"""
        return self.__cipher_key

    def create_cipher(
        self, key: str, value: int | None = None, total: int | None = None
    ):
        """create cipher"""
        self._create_cipher(key)
        if value is not None and total is not None:
            self._create_counts(value, total)

    def query_data_by_count(self, _id: int | None = None, **kwargs):
        """create query encrypt"""
        return self._query_data_by_count(_id, **kwargs)

    def decrypt(self, data: str):
        """decrypt"""
        return self._decrypt(data)

    def encrypt(self, data: str):
        """encrypt"""
        return self._encrypt(data)


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
