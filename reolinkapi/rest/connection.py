""" REST Connection """
from __future__ import annotations


import asyncio
from enum import IntEnum
import inspect
import json
import logging
from typing import Callable, Iterable, Protocol
import aiohttp

from reolinkapi.helpers.commands import isparam, iserror

from ..exceptions import (
    InvalidResponseError,
)
from ..typings.commands import CommandRequest, CommandResponse

from . import security, encrypt

from ..const import DEFAULT_TIMEOUT

_LOGGER = logging.getLogger(__name__)
_LOGGER_DATA = logging.getLogger(__name__ + ".data")


class SessionFactory(Protocol):
    """Session Factory"""

    def __call__(self, base_url: str, timeout: int) -> aiohttp.ClientSession:
        ...


def _default_create_session(base_url: str, timeout: int):
    return aiohttp.ClientSession(
        base_url=base_url,
        timeout=aiohttp.ClientTimeout(total=timeout),
        connector=aiohttp.TCPConnector(ssl=False),
    )


class Encryption(IntEnum):
    """Connection Encryption"""

    NONE = 0
    HTTPS = 1
    AES = 2


class Connection:
    """REST Connection"""

    def __init__(self, *args, session_factory: SessionFactory = None, **kwargs):
        self._disconnect_callbacks: list[Callable[[], None]] = []
        super().__init__(*args, **kwargs)
        self.__session: aiohttp.ClientSession | None = None
        self.__session_factory: SessionFactory = (
            session_factory or _default_create_session
        )
        self.__base_url = ""
        self.__hostname = ""
        self.__connection_id = 0
        other: any = self
        if isinstance(other, security.Security) and not hasattr(self, "_auth_token"):
            self._auth_token = other._auth_token
            self._has_auth_failure = other._has_auth_failure
            self.logout = other.logout
        if isinstance(other, encrypt.Encrypt) and not hasattr(self, "encrypt"):
            self._can_encrypt = other._can_encrypt
            self._encrypt = other._encrypt
            self._decrypt = other._decrypt
        elif not hasattr(self, "_can_encrypt"):
            self._can_encrypt = False

    def _create_session(self, timeout: int):
        return self.__session_factory(self.__base_url, timeout)

    @property
    def connection_id(self):
        """connection id"""
        return self.__connection_id

    @property
    def base_url(self):
        """base url"""
        return self.__base_url

    @property
    def hostname(self):
        """hostname"""
        return self.__hostname

    async def connect(
        self,
        hostname: str,
        port: int = None,
        timeout: float = DEFAULT_TIMEOUT,
        *,
        encryption: Encryption = Encryption.NONE,
    ):
        """
        setup connection to device

        full_encrypt will enable a basic cleartext encryption on all
        requests, otherwise only login will be encrypted (if supported)
        This is ignored if https is used
        """
        if port == 443 or (port is None and encryption == Encryption.HTTPS):
            https = True
            port = None
        elif port == 80 and encrypt != Encryption.HTTPS:
            https = False
            port = None
        else:
            https = encryption == Encryption.HTTPS
        scheme = "https" if https is True else "http"
        _port = f":{port}" if port is not None else ""
        url = f"{scheme}://{hostname}{_port}"
        _id = hash(url)
        if _id == self.__connection_id:
            return
        if self.__connection_id != 0:
            await self.disconnect()
        self.__base_url = url
        self.__connection_id = _id
        self.__hostname = hostname
        if https or encryption != Encryption.AES:
            self._can_encrypt = False
        if self.__session is None or self.__session.closed:
            self.__session = self._create_session(timeout)

    async def disconnect(self):
        """disconnect from device"""

        if self.__session is None:
            return
        for callback in self._disconnect_callbacks:
            if inspect.iscoroutinefunction(callback):
                await callback()
            else:
                callback()
        if not self.__session.closed:
            await self.__session.close()
        self.__connection_id = 0
        self.__base_url = ""
        self.__hostname = ""
        self.__session = None

    def _ensure_connection(self):
        if self.__session is None:
            return False

        if self.__session.closed:
            self.__session = self._create_session(self.__session.timeout.total)

        return True

    async def _execute_request(self, *args: CommandRequest, use_get: bool = False):
        """Internal API"""

        if not self._ensure_connection():
            return None

        if len(args) == 0:
            return None
        query = {"cmd": args[0]["cmd"]}
        if self._auth_token != "":
            query["token"] = self._auth_token

        headers = {"accept": "application/json"}

        cleanup = True
        response = None
        context = None
        try:
            encrypted = False
            if use_get:
                if isparam(args[0]):
                    query.update(args[0]["param"])
                _LOGGER.debug("GET: %s?%s", self.__hostname, query)
                context = self.__session.get(
                    "/cgi-bin/api.cgi",
                    params=query,
                    headers=headers,
                    allow_redirects=False,
                )
            else:
                data = self.__session.json_serialize(args)
                if self._can_encrypt:
                    edata = self._encrypt(data)
                    encrypted = data != edata
                    if encrypted:
                        query.pop("cmd", None)
                else:
                    edata = data

                _LOGGER.debug("POST: %s?%s", self.__hostname, query)
                _LOGGER_DATA.debug("%s<-%s", "E" if encrypted else "", data)
                context = self.__session.post(
                    "/cgi-bin/api.cgi",
                    params=query,
                    data=edata,
                    headers=headers,
                    allow_redirects=False,
                )

            response = await context
            if response.status >= 500:
                _LOGGER.error("got critical (%d) response code", response.status)
                raise aiohttp.ClientResponseError(
                    response.request_info,
                    [response],
                    status=response.status,
                    headers=response.headers,
                )
            if response.status >= 400:
                _LOGGER.error("got auth (%d) response code", response.status)
                raise aiohttp.ClientResponseError(
                    response.request_info,
                    [response],
                    status=response.status,
                    headers=response.headers,
                )

            cleanup = False

            return response
        except aiohttp.ClientConnectorError as http_error:
            _LOGGER.error("connection error (%s)", http_error)
            raise
        except asyncio.TimeoutError:
            _LOGGER.error("timeout")
            raise
        finally:
            if cleanup:
                if response is not None:
                    response.close()
                if context is not None:
                    context.close()

    @staticmethod
    def get_error_responses(responses: Iterable[CommandResponse]):
        """Get LocalLink Responses"""

        return filter(iserror, responses)

    async def _process_response(
        self, response: aiohttp.ClientResponse
    ) -> list[CommandResponse]:
        if response is None:
            return []

        try:
            data = await response.text()
            decrypted = False
            if self._can_encrypt and data[0] != "[":
                ddata = self._decrypt(data)
                decrypted = data != ddata
                if decrypted:
                    data = ddata

            if data[0] != "[":
                _LOGGER.error("did not get json as response: (%s)", data)
                raise InvalidResponseError()

            # handle json over text/html (missing accept?)
            data = json.loads(data)

        finally:
            response.close()

        if not isinstance(data, list):
            data = [data]
        _LOGGER_DATA.debug("%s->%s", "D" if decrypted else "", data)

        if self._auth_token != None and self._has_auth_failure(data):
            await self.logout()

        return data

    async def _execute(self, *args: CommandRequest, use_get: bool = False):
        """Internal API"""
        return await self._process_response(
            await self._execute_request(*args, use_get=use_get)
        )

    async def batch(self, commands: Iterable[CommandRequest]):
        """Execute a batch of commands"""
        return await self._execute(*commands)
