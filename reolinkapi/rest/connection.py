""" REST Connection """
from __future__ import annotations


import asyncio
import inspect
import json
import logging
from typing import Callable, Iterable, Protocol
import aiohttp

from ..exceptions import (
    InvalidCredentialsError,
    InvalidResponseError,
    ReolinkError,
)
from .typings.commands import CommandRequest, CommandResponse

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


CACHE_CONNECTION_ID = "connection_id"
CACHE_URL = "url"


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
        self._https = False
        other: any = self
        if isinstance(other, security.Security) and not hasattr(self, "_auth_token"):
            self._auth_token = other._auth_token
        if isinstance(other, encrypt.Encrypt):
            self.__can_encrypt = True
            if not hasattr(self, "encrypt"):
                self._encrypt = other._encrypt
                self._decrypt = other._decrypt

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
        https: bool = None,
    ):
        """
        setup connection to device
        """
        if port == 443 or (port is None and https):
            https = True
            port = None
        elif port == 80 and https is not True:
            https = False
            port = None
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
        self._https = https
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
        self._https = False
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
        try:
            if use_get:
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
                _LOGGER.debug("POST: %s?%s", self.__hostname, query)
                _LOGGER_DATA.debug("<-%s", data)
                if self.__can_encrypt and not self._https:
                    data = self._encrypt(data)
                    encrypted = True
                context = self.__session.post(
                    "/cgi-bin/api.cgi",
                    params=query,
                    data=data,
                    headers=headers,
                    allow_redirects=False,
                )

            response = await context
            if response.status >= 500:
                _LOGGER.error("got critical (%d) response code", response.status)
                raise InvalidResponseError()
            if response.status >= 400:
                _LOGGER.error("got auth (%d) response code", response.status)
                raise InvalidCredentialsError()

            cleanup = False
            return (response, bool(encrypted))
        except aiohttp.ClientConnectorError as http_error:
            _LOGGER.error("connection error (%s)", http_error)
            raise ReolinkError(http_error) from None
        except asyncio.TimeoutError:
            _LOGGER.error("timeout")
            raise
        except Exception as _e:
            _LOGGER.error("Unhnandled exception (%s)", _e)
            raise ReolinkError(_e) from None
        finally:
            if cleanup:
                if response is not None:
                    response.close()
                context.close()

    async def _process_response(
        self, response: aiohttp.ClientResponse, encrypted: bool = False
    ) -> list[CommandResponse]:
        if response is None:
            return []

        try:
            data = await response.text()
            if self.__can_encrypt and encrypted and data[0] != "[":
                data = self._decrypt(data)

            if data[0] != "[":
                _LOGGER.error("did not get json as response: (%s)", data)
                raise InvalidResponseError()

            # handle json over text/html (missing accept?)
            data = json.loads(data)

        finally:
            response.close()

        if not isinstance(data, list):
            data = [data]
        _LOGGER_DATA.debug("->%s", data)
        return data

    async def _execute(self, *args: CommandRequest, use_get: bool = False):
        """Internal API"""
        return await self._process_response(
            *(await self._execute_request(*args, use_get=use_get))
        )

    async def batch(self, commands: Iterable[CommandRequest]):
        """Execute a batch of commands"""
        return await self._execute(*commands)
