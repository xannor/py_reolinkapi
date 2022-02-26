""" REST Connection """

import asyncio
from dataclasses import MISSING
import inspect
from json import loads
import logging
from typing import Callable, Optional
import aiohttp

from ..exceptions import InvalidCredentials, InvalidResponse, ReolinkException
from ..utils.dataclasses import DataclassesJSONEncoder, fromdict, isdictof

from .command import (
    CommandRequest,
    CommandValueResponse,
    UnknownCommandResponse,
    CommandError,
    get_response_type,
)

from ..meta.auth import AuthenticationInterface
from ..const import DEFAULT_TIMEOUT

_LOGGER = logging.getLogger(__name__)
_LOGGER_DATA = logging.getLogger(__name__ + ".data")


class Connection:
    """REST Connection"""

    def __init__(self) -> None:
        self._disconnect_callbacks: list[Callable[[], None]] = []
        super().__init__()
        self._url: Optional[str] = None
        self._session: Optional[aiohttp.ClientSession] = None
        self.__json_encoder = DataclassesJSONEncoder()
        if isinstance(self, AuthenticationInterface):
            self.__get_auth_token = self._get_auth_token

    def _get_disconnect_callbacks(self):
        return self._disconnect_callbacks

    def _create_session(self, timeout):

        return aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=timeout),
            connector=aiohttp.TCPConnector(ssl=False),
            json_serialize=self.__json_encoder.encode,
        )

    async def connect(
        self,
        hostname: str,
        port: int = MISSING,
        timeout: float = DEFAULT_TIMEOUT,
        **kwargs,
    ):
        """
        setup connection to device

        https(bool) is an optional keyword argument needed if using an https connection
        """
        await self.disconnect()
        https = bool(kwargs["https"]) if "https" in kwargs else MISSING
        if port == 443 or (port is MISSING and https):
            https = True
            port = MISSING
        elif port == 80 and https is not True:
            https = False
            port = MISSING
        scheme = "https" if https is True else "http"
        _port = f":{port}" if port is not MISSING else ""
        self._url = f"{scheme}://{hostname}{_port}/cgi-bin/api.cgi"
        self._session = self._create_session(timeout)

    async def disconnect(self):
        """disconnect from device"""

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
        self._url = None

    def _ensure_connection(self):
        if self._session is None:
            return False

        if self._session.closed:
            self._session = self._create_session(self._session.timeout.total)

        return True

    async def _execute(self, *args: CommandRequest, **kwargs):
        """
        Internal API

        get(bool) can be specified to use a GET request instead of a POST
        """
        if not self._ensure_connection():
            return []

        if len(args) == 0:
            return []
        query = {"cmd": args[0].command}
        token = self.__get_auth_token()
        if token is not None:
            query["token"] = token

        types = {
            req.command: get_response_type(req) or UnknownCommandResponse
            for req in args
        }

        def map_response(__dict: dict):
            if isdictof(__dict, CommandError):
                return fromdict(__dict, CommandError)
            if not isdictof(__dict, CommandValueResponse):
                raise InvalidResponse()
            command = __dict.get("cmd")
            _type = types.get(command, UnknownCommandResponse)
            return fromdict(__dict, _type)

        headers = {"accept": "application/json"}

        use_get = bool(kwargs["get"]) if "get" in kwargs else False
        data = self._session.json_serialize(args)
        _LOGGER_DATA.debug("%s", data)
        try:
            if use_get:
                query["params"] = data
                context = self._session.get(
                    self._url, params=query, headers=headers, allow_redirects=False
                )
            else:
                context = self._session.post(
                    self._url,
                    params=query,
                    data=data,
                    headers=headers,
                    allow_redirects=False,
                )

            async with context as response:
                if response.status >= 500:
                    _LOGGER.error("got critical (%d) response code", response.status)
                    raise InvalidResponse()
                if response.status >= 400:
                    _LOGGER.error("got auth (%d) response code", response.status)
                    raise InvalidCredentials()

                if response.content_type == "appliction/json":
                    data = await response.json()
                elif response.content_type == "text/html":
                    data = await response.text()

                    if data[0] != "[":
                        _LOGGER.error("did not get json as response: (%s)", data)
                        raise InvalidResponse()

                    # handle json over text/html (missing accept?)
                    data = loads(data)
                else:
                    raise InvalidResponse()

                if not isinstance(data, list):
                    data = [data]

                _LOGGER_DATA.debug(data)

                return list(map(map_response, data))

        except aiohttp.ClientConnectorError as http_error:
            _LOGGER.error("connection error (%s)", http_error)
            raise ReolinkException(http_error)
        except asyncio.TimeoutError:
            _LOGGER.error("timeout")
            raise
        except Exception as _e:
            _LOGGER.error("Unhnandled exception (%s)", _e)
            raise ReolinkException(_e)
