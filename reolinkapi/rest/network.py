"""Network Mixin"""
from __future__ import annotations


from typing import TypedDict
from urllib.parse import quote_plus

from .connection import Connection, CACHE_TOKEN

from .typings.commands import CommandRequest, CommandRequestTypes
from .typings.network import ChannelStatus, LinkInfo, NetworkPorts, RTSPUrls

from .const import StreamTypes


class GetLocalLinkResponseValue(TypedDict):
    """Get Local Link Response Value"""

    LocalLink: LinkInfo


GET_LOCAL_LINK_COMMAND = "GetLocalLink"


class GetChannelStatusResponseValue(TypedDict):
    """Get Channel Status Response Value"""

    count: int
    status: list[ChannelStatus]


GET_CHANNEL_STATUS_COMMAND = "GetChannelStatus"


class GetRTSPUrlCommandResponseValue(TypedDict):
    """Get RTSP Command Response Value"""

    rtspUrl: RTSPUrls


GET_RTSP_URL_COMMAND = "GetRtspUrl"


class GetNetworkPortsCommandResponseValue(TypedDict):
    """Get Network Ports Command Response Value"""

    NetPort: NetworkPorts


GET_NETWORK_PORT_COMMAND = "GetNetPort"

CACHE_PORTS = "ports"
CACHE_LINK = "link"

_CACHE_NORTSP = "_no_get_rtsp"


class _LocalCache(TypedDict):
    ports: NetworkPorts
    link: LinkInfo
    token: str
    _no_get_rtsp: bool


class Network:
    """Network commands Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cache: _LocalCache = (
            getattr(self, "__cache") if hasattr(self, "__cache") else {}
        )
        setattr(self, "__cache", self.__cache)
        if isinstance(self, Connection) and not hasattr(self, "_execute"):
            # type "interface"
            self._execute = self._execute

    async def get_local_link(self):
        """Get Local Link"""

        self.__cache.pop(CACHE_LINK, None)
        results = await self._execute(
            CommandRequest(
                cmd=GET_LOCAL_LINK_COMMAND, action=CommandRequestTypes.VALUE_ONLY
            )
        )
        if (
            len(results) != 1
            or not isinstance(results[0], dict)
            or results[0]["cmd"] != GET_LOCAL_LINK_COMMAND
        ):
            return None

        value: GetLocalLinkResponseValue = results[0]["value"]
        self.__cache[CACHE_LINK] = value["LocalLink"]
        return value["LocalLink"]

    async def get_channel_status(self):
        """Get Local Link"""

        results = await self._execute(
            CommandRequest(
                cmd=GET_CHANNEL_STATUS_COMMAND, action=CommandRequestTypes.VALUE_ONLY
            )
        )
        if (
            len(results) != 1
            or not isinstance(results[0], dict)
            or results[0]["cmd"] != GET_CHANNEL_STATUS_COMMAND
        ):
            return None

        value: GetChannelStatusResponseValue = results[0]["value"]

        if value["count"] != len(value["status"]):
            pass  # TODO assert if mismatch? is this an issue?
        return value["status"]

    async def get_ports(self):
        """Get RTSP Url"""

        self.__cache.pop(CACHE_PORTS, None)
        results = await self._execute(
            CommandRequest(
                cmd=GET_NETWORK_PORT_COMMAND, action=CommandRequestTypes.VALUE_ONLY
            )
        )
        if (
            len(results) != 1
            or not isinstance(results[0], dict)
            or results[0]["cmd"] != GET_NETWORK_PORT_COMMAND
        ):
            return None

        value: GetNetworkPortsCommandResponseValue = results[0]["value"]
        self.__cache[CACHE_PORTS] = value["NetPort"]
        return value["NetPort"]

    async def get_rtsp_url(
        self, channel: int = 0, stream: StreamTypes = StreamTypes.MAIN
    ):
        """Get RTSP Url"""

        if _CACHE_NORTSP not in self.__cache:
            results = await self._execute(
                CommandRequest(
                    cmd=GET_RTSP_URL_COMMAND, action=CommandRequestTypes.VALUE_ONLY
                )
            )
            if (
                len(results) == 1
                and isinstance(results[0], dict)
                and results[0]["cmd"] == GET_RTSP_URL_COMMAND
            ):
                value: GetRTSPUrlCommandResponseValue = results[0]["value"]
                return value["rtspUrl"]

            self.__cache["_no_get_rtsp"] = True

        link = (
            self.__cache["link"]
            if CACHE_LINK in self.__cache
            else await self.get_local_link()
        )
        ports = (
            self.__cache["ports"]
            if CACHE_PORTS in self.__cache
            else await self.get_ports()
        )

        port = (
            f":{ports.rtsp.port}"
            if ports.rtsp.enabled and ports.rtsp.port > 0 and ports.rtsp.port != 554
            else ""
        )

        url = f"rtsp://{link.ipv4.address}{port}/h264Preview_{channel:02}_{stream.name.lower()}"
        if CACHE_TOKEN in self.__cache:
            return f"{url}&Token={quote_plus(self.__cache['token'])}"
        return url

    async def get_rtmp_url(
        self, channel: int = 0, stream: StreamTypes = StreamTypes.MAIN
    ):
        """Get RTMP Url"""

        link = (
            self.__cache["link"]
            if CACHE_LINK in self.__cache
            else await self.get_local_link()
        )
        ports = (
            self.__cache["ports"]
            if CACHE_PORTS in self.__cache
            else await self.get_ports()
        )
        port = (
            f":{ports.rtmp.port}"
            if ports.rtmp.enabled and ports.rtmp.port > 0 and ports.rtmp.port != 1935
            else ""
        )

        url = f"rtmp://{link.ipv4.address}{port}/bcs/channel{channel}_{stream.name.lower()}.bcs?channel={channel}&stream={stream}"
        if CACHE_TOKEN in self.__cache:
            return f"{url}&Token={quote_plus(self.__cache['token'])}"
        return url
