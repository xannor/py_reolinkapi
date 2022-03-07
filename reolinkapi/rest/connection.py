""" REST Connection """
from __future__ import annotations


import asyncio
import inspect
import json
import logging
from typing import Callable, Iterable, Protocol, TypedDict
import aiohttp

from ..exceptions import (
    InvalidCredentialsError,
    InvalidResponseError,
    ReolinkError,
)
from .typings.commands import CommandRequest, CommandResponse
from .security import CACHE_TOKEN

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


class _LocalCache(TypedDict):
    token: str
    url: str
    connection_id: int
    hostname: str


CACHE_CONNECTION_ID = "connection_id"


class Connection:
    """REST Connection"""

    def __init__(self, *args, session_factory: SessionFactory = None, **kwargs):
        self._disconnect_callbacks: list[Callable[[], None]] = []
        super().__init__(*args, **kwargs)
        self.__cache: _LocalCache = (
            getattr(self, "__cache") if hasattr(self, "__cache") else {}
        )
        setattr(self, "__cache", self.__cache)
        self._session: aiohttp.ClientSession | None = None
        self._session_factory: SessionFactory = (
            session_factory or _default_create_session
        )

    def _create_session(self, timeout: int):
        return self._session_factory(self.__cache["url"], timeout)

    @property
    def connection_id(self) -> int:
        """connection id"""
        return self.__cache["connection_id"] if "connection_id" in self.__cache else 0

    @property
    def base_url(self) -> str:
        """base url"""
        return self.__cache["url"] if "url" in self.__cache else ""

    async def connect(
        self,
        hostname: str,
        port: int = None,
        timeout: float = DEFAULT_TIMEOUT,
        **kwargs,
    ):
        """
        setup connection to device

        https(bool) is an optional keyword argument needed if using an https connection
        """
        https = bool(kwargs["https"]) if "https" in kwargs else None
        if port == 443 or (port is None and https):
            https = True
            port = None
        elif port == 80 and https is not True:
            https = False
            port = None
        scheme = "https" if https is True else "http"
        _port = f":{port}" if port is not None else ""
        _url = f"{scheme}://{hostname}{_port}"
        _id = hash(_url)
        if CACHE_CONNECTION_ID in self.__cache and _id == self.__cache["connection_id"]:
            return
        if CACHE_CONNECTION_ID in self.__cache:
            await self.disconnect()
        self.__cache["url"] = _url
        self.__cache["connection_id"] = _id
        self.__cache["hostname"] = hostname
        if self._session is None or self._session.closed:
            self._session = self._create_session(timeout)

    async def disconnect(self):
        """disconnect from device"""

        self.__cache.clear()
        if self._session is None:
            return
        for callback in self._disconnect_callbacks:
            if inspect.iscoroutinefunction(callback):
                await callback()
            else:
                callback()
        if not self._session.closed:
            await self._session.close()
        self._session = None

    def _ensure_connection(self):
        if self._session is None:
            return False

        if self._session.closed:
            self._session = self._create_session(self._session.timeout.total)

        return True

    async def _execute_response(self, *args: CommandRequest, use_get: bool = False):
        """Internal API"""

        if not self._ensure_connection():
            return None

        if len(args) == 0:
            return None
        query = {"cmd": args[0]["cmd"]}
        if CACHE_TOKEN in self.__cache:
            query["token"] = self.__cache["token"]

        headers = {"accept": "application/json"}

        cleanup = True
        try:
            if use_get:
                query.update(args[0]["param"])
                _LOGGER.debug("GET: %s?%s", self.__cache["hostname"], query)
                context = self._session.get(
                    "/cgi-bin/api.cgi",
                    params=query,
                    headers=headers,
                    allow_redirects=False,
                )
            else:
                data = self._session.json_serialize(args)
                _LOGGER.debug("POST: %s?%s", self.__cache["hostname"], query)
                _LOGGER_DATA.debug("<-%s", data)
                context = self._session.post(
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
            return response
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

    async def _execute(
        self, *args: CommandRequest, use_get: bool = False
    ) -> list[CommandResponse]:
        """Internal API"""
        response = await self._execute_response(*args, use_get=use_get)
        if response is None:
            return []

        try:
            if response.content_type == "appliction/json":
                data = await response.json()
            elif response.content_type == "text/html":
                data = await response.text()

                if data[0] != "[":
                    _LOGGER.error("did not get json as response: (%s)", data)
                    raise InvalidResponseError()

                # handle json over text/html (missing accept?)
                data = json.loads(data)
            else:
                raise InvalidResponseError()

        finally:
            response.close()

        if not isinstance(data, list):
            data = [data]
        _LOGGER_DATA.debug("->%s", data)
        return data

    async def batch(self, commands: Iterable[CommandRequest]):
        """Execute a batch of commands"""
        return await self._execute(*commands)
