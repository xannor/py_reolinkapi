""" REST Connection """
from __future__ import annotations


import asyncio
from enum import IntEnum
import inspect
import json
import logging
from typing import Callable, Iterable, Protocol
from urllib.parse import urlparse
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
            self._auth_failed = other._auth_failed

        if isinstance(other, encrypt.Encrypt) and not hasattr(self, "encrypt"):
            self._can_encrypt = other._can_encrypt
            self._encrypt = other._encrypt
            self._decrypt = other._decrypt
            self._query_data_by_count = other._query_data_by_count
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
    def secured(self):
        """Secure connection"""
        return self.__base_url.startswith("https:")

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
        await self._setup_connection(
            hostname, port, timeout, https, encryption == Encryption.AES
        )

    async def _setup_connection(
        self,
        hostname: str,
        port: int | None,
        timeout: float,
        https: bool,
        can_encrypt: bool,
        full_reset: bool = True,
    ):
        scheme = "https" if https is True else "http"
        _port = f":{port}" if port is not None else ""
        url = f"{scheme}://{hostname}{_port}"
        _id = hash(url)
        if _id == self.__connection_id:
            return
        if self.__connection_id != 0:
            if full_reset:
                await self.disconnect()
            else:
                await self.__session.close()

        self.__base_url = url
        self.__connection_id = _id
        self.__hostname = hostname
        if https or not can_encrypt:
            self._can_encrypt = False
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
        if use_get and isparam(args[0]):
            query.update(args[0]["param"])
        url = "/cgi-bin/api.cgi"
        if args[0]["cmd"] == security.LOGIN_COMMAND:
            url += f'?cmd={args[0]["cmd"]}'
        elif self._auth_token != "":
            url += f"?token={self._auth_token}"
        count = None
        if self._can_encrypt:
            (count, enc) = self._query_data_by_count(
                *(f"{_k}={_v}" for _k, _v in query.items())
            )
            if enc:
                count.free = False
                url += f"&encrypt={enc}"
                query.clear()

        headers = {"Accept": "*/*", "Content-Type": "application/json"}

        cleanup = True
        response = None
        context = None
        try:
            encrypted = False
            if use_get:
                _LOGGER.debug("GET: %s<-%s", url, query)
                context = self.__session.get(
                    url,
                    params=query,
                    headers=headers,
                    allow_redirects=False,
                )
            else:
                data = self.__session.json_serialize(args)
                if self._can_encrypt:
                    edata = self._encrypt(data)
                    encrypted = data != edata
                else:
                    edata = data

                _LOGGER_DATA.debug(
                    "%s%s<-%s", self.__hostname, "(E)" if encrypted else "", data
                )
                context = self.__session.post(
                    url,
                    data=edata,
                    headers=headers,
                    allow_redirects=False,
                )

            response = await context
            if count is not None:
                count.free = True
            if response.status in (302, 301) and "location" in response.headers:
                location = response.headers["location"]
                redir = urlparse(location)
                base = urlparse(self.__base_url)
                if (
                    base.scheme != redir.scheme
                    and base.scheme == "http"
                    or redir.scheme == "http"
                ):
                    if redir.scheme == "http":
                        _LOGGER.warning(
                            "Got http redirect from camera (%s), please verify configuration",
                            self.__base_url,
                        )
                        await self._setup_connection(
                            redir.hostname,
                            redir.port,
                            self.__session.timeout.total,
                            False,
                            True,
                        )
                    else:
                        _LOGGER.warning(
                            "Got https redirect from camera (%s), please verify configuration",
                            self.__base_url,
                        )
                        await self._setup_connection(
                            redir.hostname,
                            redir.port,
                            self.__session.timeout.total,
                            True,
                            True,
                        )
                    return await self._execute_request(*args)

                _LOGGER.error(
                    "got unexpected redirect from camera (%s), please verify configurtation",
                    self.__base_url,
                )
                raise aiohttp.ClientResponseError(
                    response.request_info,
                    [response],
                    status=response.status,
                    headers=response.headers,
                )

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
        except Exception as e:
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
            self._auth_failed = True

        return data

    async def _execute(self, *args: CommandRequest, use_get: bool = False):
        """Internal API"""
        return await self._process_response(
            await self._execute_request(*args, use_get=use_get)
        )

    async def batch(self, commands: Iterable[CommandRequest]):
        """Execute a batch of commands"""
        return await self._execute(*commands)
