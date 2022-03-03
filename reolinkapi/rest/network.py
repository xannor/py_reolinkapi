"""Network Mixin"""
from __future__ import annotations


from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar, Mapping
from urllib.parse import quote_plus

from reolinkapi.utils.mappings import Wrapped

from ..utils.dataclasses import flatten, keyword

from .command import (
    CommandRequest,
    CommandRequestChannelParam,
    CommandValueResponse,
    CommandValueResponseValue,
    response_type,
)
from ..meta.connection import ConnectionInterface
from ..meta.auth import AuthenticationInterface

from .const import StreamTypes


class LinkType(Enum):
    """Link Type"""

    STATIC = "Static"
    DHCP = "DHCP"


@dataclass
class LinkIPV4:
    """IPV4 network info"""

    gateway: str = field(default="192.168.0.1")
    address: str = field(default="192.168.0.100", metadata=keyword("ip"))
    mask: str = field(default="255.255.255.0")


@dataclass
class LinkInfo:
    """LinkInfo"""

    active: str = field(default="", metadata=keyword("activeLink"))
    mac_address: str = field(default="", metadata=keyword("mac"))
    type: LinkType = field(default_factory=LinkType)
    ipv4: LinkIPV4 = field(default_factory=LinkIPV4, metadata=keyword("static"))


@dataclass
class LocalLinkResponseValue(CommandValueResponseValue):
    """Local Link Response Value"""

    info: LinkInfo = field(default_factory=LinkInfo, metadata=keyword("LocalLink"))


@dataclass
class LocalLinkResponse(CommandValueResponse):
    """Local Link Response"""

    value: LocalLinkResponseValue = field(default_factory=LocalLinkResponseValue)


@dataclass
@response_type(LocalLinkResponse)
class LocalLinkRequest(CommandRequest):
    """Local Link Request"""

    COMMAND: ClassVar = "GetLocalLink"

    def __post_init__(self):
        self.command = type(self).COMMAND
        self.param = None


@dataclass
class ChannelStatus:
    """Channel Status"""

    channel: int = field(default=0)
    name: str = field(default="")
    online: bool = field(default=False)
    type_info: str = field(default="", metadata=keyword("typeInfo"))


@dataclass
class ChannelStatusResponseValue(CommandValueResponseValue):
    """Channel Status Response Value"""

    count: int = field(default=0)
    channels: list[ChannelStatus] = field(
        default_factory=list, metadata=keyword("status")
    )


@dataclass
class ChannelStatusResponse(CommandValueResponse):
    """Channel Status Response"""

    value: ChannelStatusResponseValue = field(
        default_factory=ChannelStatusResponseValue
    )


@dataclass
@response_type(ChannelStatusResponse)
class ChannelStatusRequest(CommandRequest):
    """Channel Status Request"""

    COMMAND: ClassVar = "GetChannelstatus"

    def __post_init__(self):
        self.command = type(self).COMMAND
        self.param = None


@dataclass
class RTSPUrls(Wrapped[StreamTypes, str]):
    """Urls"""

    def update(self, *args, **kwargs):
        def _make_key(key: StreamTypes | str | int):
            if isinstance(key, str):
                if key[-6:] != "Stream":
                    raise KeyError(key)
                key = key[0:6].upper()
                return StreamTypes[key]
            return StreamTypes(key)

        super.update(
            *((_make_key(k), v) for k, v in args),
            **{_make_key(k): v for k, v in kwargs.items()},
        )


@dataclass
class RTSPInfo:
    """RTSP Url Information"""

    channel: int = field(default=0)
    url: Mapping[StreamTypes, str] = field(
        default_factory=RTSPUrls,
        metadata=flatten(),
    )


@dataclass
class RTSPResponseValue(CommandValueResponseValue):
    """RTSP Url Response Value"""

    info: RTSPInfo = field(default_factory=RTSPInfo, metadata=keyword("rtspUrl"))


@dataclass
class RTSPUrlResponse(CommandValueResponse):
    """RTSP Url Response"""

    value: RTSPResponseValue = field(default_factory=RTSPResponseValue)


@dataclass
@response_type(RTSPUrlResponse)
class RTSPUrlRequest(CommandRequest):
    """RTSP Url Request"""

    COMMAND: ClassVar = "GetRtspUrl"
    param: CommandRequestChannelParam = field(
        default_factory=CommandRequestChannelParam
    )

    def __post_init__(self):
        self.command = type(self).COMMAND


@dataclass
class PortStatus:
    """Network Port Status"""

    enabled: bool = field(default=True, metadata=keyword("Enable"))
    port: int = field(default=0, metadata=keyword("Port"))


@dataclass
class NetworkPorts:
    """Network Ports"""

    http: PortStatus = field(default_factory=PortStatus, metadata=flatten(True))
    https: PortStatus = field(default_factory=PortStatus, metadata=flatten(True))
    media: PortStatus = field(
        default_factory=lambda: PortStatus(True), metadata=flatten(True)
    )
    onvif: PortStatus = field(default_factory=PortStatus, metadata=flatten(True))
    rtmp: PortStatus = field(default_factory=PortStatus, metadata=flatten(True))
    rtsp: PortStatus = field(default_factory=PortStatus, metadata=flatten(True))


@dataclass
class GetNetworkPortResponseValue(CommandValueResponseValue):
    """Get Network Port Response Value"""

    info: NetworkPorts = field(
        default_factory=NetworkPorts, metadata=keyword("NetPort")
    )


@dataclass
class GetNetworkPortResponse(CommandValueResponse):
    """Get Network Port Response"""

    value: GetNetworkPortResponseValue = field(
        default_factory=GetNetworkPortResponseValue
    )


@dataclass
@response_type(GetNetworkPortResponse)
class GetNetworkPortRequest(CommandRequest):
    """Get Network Port Request"""

    COMMAND: ClassVar = "GetNetPort"

    def __post_init__(self):
        self.command = type(self).COMMAND
        self.param = None


class Network:
    """Network commands Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__cache = {}
        if isinstance(self, ConnectionInterface) and not hasattr(self, "_execute"):
            # type "interface"
            self._execute = self._execute
        if isinstance(self, AuthenticationInterface) and not hasattr(
            self, "_get_auth_token"
        ):
            # type "itnerface"
            self._get_auth_token = self._get_auth_token
        elif not hasattr(self, "_get_auth_token"):
            self._get_auth_token = lambda: None

    async def get_local_link(self):
        """Get Local Link"""

        self.__cache.pop("link", None)
        results = await self._execute(LocalLinkRequest())
        if len(results) != 1 or not isinstance(results[0], LocalLinkResponse):
            return None

        result = results[0].value.info
        self.__cache["link"] = result
        return result

    async def get_channel_status(self):
        """Get Local Link"""

        results = await self._execute(ChannelStatusRequest())
        if len(results) != 1 or not isinstance(results[0], ChannelStatusResponse):
            return None

        if results[0].value.count != len(results[0].value.channels):
            pass  # TODO assert if mismatch? is this an issue?
        return results[0].value.channels

    async def get_ports(self):
        """Get RTSP Url"""

        self.__cache.pop("ports", None)
        results = await self._execute(GetNetworkPortRequest())
        if len(results) != 1 or not isinstance(results[0], GetNetworkPortResponse):
            return None

        result = results[0].value.info
        self.__cache["ports"] = result
        return results

    async def get_rtsp_url(
        self, channel: int = 0, stream: StreamTypes = StreamTypes.MAIN
    ):
        """Get RTSP Url"""

        if "_no_get_rtsp" not in self.__cache:
            results = await self._execute(
                RTSPUrlRequest(CommandRequestChannelParam(channel))
            )
            if len(results) == 1 and isinstance(results[0], RTSPUrlResponse):
                return results[0].value.info.url[stream]
            self.__cache["_no_get_rtsp"] = True

        link: LinkInfo = (
            self.__cache["link"]
            if "link" in self.__cache
            else await self.get_local_link()
        )
        ports: NetworkPorts = (
            self.__cache["ports"] if "ports" in self.__cache else await self.get_ports()
        )
        port = (
            f":{ports.rtsp.port}"
            if ports.rtsp.enabled and ports.rtsp.port > 0 and ports.rtsp.port != 554
            else ""
        )

        url = f"rtsp://{link.ipv4.address}{port}/h264Preview_{channel:02}_{stream.name.lower()}"
        auth = self._get_auth_token()
        if auth is not None:
            return f"{url}&Token={quote_plus(auth)}"
        return url

    async def get_rtmp_url(
        self, channel: int = 0, stream: StreamTypes = StreamTypes.MAIN
    ):
        """Get RTMP Url"""

        link: LinkInfo = (
            self.__cache["link"]
            if "link" in self.__cache
            else await self.get_local_link()
        )
        ports: NetworkPorts = (
            self.__cache["ports"] if "ports" in self.__cache else await self.get_ports()
        )
        port = (
            f":{ports.rtmp.port}"
            if ports.rtmp.enabled and ports.rtmp.port > 0 and ports.rtmp.port != 1935
            else ""
        )

        url = f"rtmp://{link.ipv4.address}{port}/bcs/channel{channel}_{stream.name.lower()}.bcs?channel={channel}&stream={stream}"
        auth = self._get_auth_token()
        if auth is not None:
            return f"{url}&Token={quote_plus(auth)}"
        return url
