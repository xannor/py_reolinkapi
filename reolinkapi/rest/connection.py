""" REST Connection """

import asyncio
import inspect
from json import loads
import logging
from typing import Callable, Optional
import aiohttp

from ..exceptions import InvalidCredentials, InvalidResponse, ReolinkException
from ..utils.dataclasses import DataclassesJSONEncoder, asdict, fromdict, isdictof

from .command import (
    CommandRequest,
    CommandStreamResponse,
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

    def __init__(self, *args, **kwargs):
        self._disconnect_callbacks: list[Callable[[], None]] = []
        super().__init__(*args, **kwargs)
        self._url: Optional[str] = None
        self._session: Optional[aiohttp.ClientSession] = None
        self.__json_encoder = DataclassesJSONEncoder()
        self._connection_hash: int = 0
        if isinstance(self, AuthenticationInterface) and not hasattr(
            self, "_get_auth_token"
        ):
            self._get_auth_token = self._get_auth_token

    def _get_disconnect_callbacks(self):
        return self._disconnect_callbacks

    def _create_session(self, timeout):

        return aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=timeout),
            connector=aiohttp.TCPConnector(ssl=False),
            json_serialize=self.__json_encoder.encode,
        )

    @property
    def connection_id(self):
        """connection id"""
        return self._connection_hash

    @property
    def base_url(self):
        """device url"""
        return self._url or ""

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
        if _url != self._url:
            await self.disconnect()
        self._url = _url
        self._connection_hash = hash(self._url)
        if self._session is None or self._session.closed:
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
        token = self._get_auth_token()
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
        url = f"{self._url}/cgi-bin/api.cgi"
        try:
            if use_get:
                query.update(asdict(args[0].param))
                _LOGGER.debug("GET: %s?%s", url, query)
                context = self._session.get(
                    url, params=query, headers=headers, allow_redirects=False
                )
            else:
                data = self._session.json_serialize(args)
                _LOGGER.debug("Post: %s?%s", url, query)
                _LOGGER_DATA.debug("%s", data)
                context = self._session.post(
                    url,
                    params=query,
                    data=data,
                    headers=headers,
                    allow_redirects=False,
                )

            cleanup = True
            response = await context
            try:
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
                    cleanup = False
                    return [
                        CommandStreamResponse(
                            response.content,
                            content_length=response.content_length,
                            content_type=response.content_type,
                            content_disposition=response.content_disposition,
                        )
                    ]

                if not isinstance(data, list):
                    data = [data]

                _LOGGER_DATA.debug(data)

                return list(map(map_response, data))
            finally:
                if cleanup:
                    response.close()
                    context.close()

        except aiohttp.ClientConnectorError as http_error:
            _LOGGER.error("connection error (%s)", http_error)
            raise ReolinkException(http_error)
        except asyncio.TimeoutError:
            _LOGGER.error("timeout")
            raise
        except Exception as _e:
            _LOGGER.error("Unhnandled exception (%s)", _e)
            raise ReolinkException(_e)
