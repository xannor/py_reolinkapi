"""Network 3.3"""
from __future__ import annotations

from typing import Final, TypedDict
from typing_extensions import TypeGuard

try:
    from enum import StrEnum  # pylint: disable=ungrouped-imports
except ImportError:
    from backports.strenum import StrEnum

from .commands import (
    CommandRequest,
    CommandRequestTypes,
)

from .const import IntStreamTypes

from . import connection, security


class LinkType(StrEnum):
    """Link Type"""

    STATIC = "Static"
    DHCP = "DHCP"


class IPInfoType(TypedDict, total=False):
    """IP Information"""

    gateway: str
    ip: str
    mask: str


class LinkInfoType(TypedDict, total=False):
    """Link Information"""

    activeLink: str
    mac: str
    type: str
    static: IPInfoType


class ChannelStatusType(TypedDict, total=False):
    """Channel Status"""

    channel: int
    name: str
    online: bool
    typeInfo: str


class RTSPUrlsType(TypedDict, total=False):
    """RTSP Url Info"""

    channel: int
    mainStream: str
    subStream: str
    extStream: str


class NetworkPortsType(TypedDict, total=False):
    """Network Ports"""

    httpEnable: bool
    httpPort: int
    httpsEnable: bool
    httpsPort: int
    mediaEnable: bool
    mediaPort: int
    onvifEnable: bool
    onvifPort: int
    rtmpEnable: bool
    rtmpPort: int
    rtspnable: bool
    rtspPort: int


class P2PInfoType(TypedDict, total=False):
    """P2P Info"""

    enable: bool
    uid: str


class Network:
    """Network commands Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__link: LinkInfoType | None = None
        self.__ports: NetworkPortsType | None = None
        self.__no_get_rtsp = False
        if isinstance(self, connection.Connection):
            self._disconnect_callbacks.append(self.__clear)

    def __clear(self):
        self.__no_get_rtsp = False
        self.__link = None
        self.__ports = None

    async def get_local_link(self):
        """Get Local Link"""

        self.__link = None
        self.__ports = None
        if isinstance(self, connection.Connection):
            responses = await self._execute(GetLocalLinkCommand())
        else:
            return None

        link = next(map(GetLocalLinkCommand.get_response, filter(
            GetLocalLinkCommand.is_response, responses)), None)
        if link is not None:
            self.__link = link
        return link

    async def get_channel_status(self):
        """Get Channel Statuses Link"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(GetChannelStatusCommand())
        else:
            return None

        status = next(map(GetChannelStatusCommand.get_response, filter(
            GetChannelStatusCommand.is_response, responses)), None)
        if status is not None:
            return status["status"]

    async def get_ports(self):
        """Get Network Ports Url"""

        self.__ports = None
        if isinstance(self, connection.Connection):
            responses = await self._execute(GetNetworkPortsCommand())
        else:
            return None

        ports = next(map(GetNetworkPortsCommand.get_response, filter(
            GetNetworkPortsCommand.is_response, responses)), None)
        if ports is not None:
            self.__ports = ports
        return ports

    async def _ensure_ports_and_link(self):
        commands = []
        if self.__link is None:
            commands.append(GetLocalLinkCommand())
        if self.__ports is None:
            commands.append(GetNetworkPortsCommand())

        if len(commands) > 0 and isinstance(self, connection.Connection):
            responses = await self._execute(*commands)
        else:
            responses = []

        link = next(map(GetLocalLinkCommand.get_response, filter(
            GetLocalLinkCommand.is_response, responses)), None)
        ports = next(map(GetNetworkPortsCommand.get_response, filter(
            GetNetworkPortsCommand.is_response, responses)), None)
        if link is not None:
            self.__link = link
        if ports is not None:
            self.__ports = ports

    async def get_rtsp_url(
        self, channel: int = 0, stream: IntStreamTypes = IntStreamTypes.MAIN
    ):
        """Get RTSP Url"""

        if not self.__no_get_rtsp:
            responses = None
            if isinstance(self, connection.Connection):
                responses = await self._execute(GetRTSPUrlsCommand())

            if responses is not None:
                urls = next(map(GetRTSPUrlsCommand.get_response, filter(
                    GetRTSPUrlsCommand.is_response, responses)), None)
                if not urls is None:
                    url: str = urls[f"{stream.name.lower()}Stream"]
                    # if isinstance(self, security.Security) and self._auth_token != "":
                    #    return f"{url}&token={self._auth_token}"
                    return url

            self.__no_get_rtsp = True

        await self._ensure_ports_and_link()

        port = (
            f':{self.__ports["rtspPort"]}'
            if self.__ports["rtspPort"] not in (0, 554)
            else ""
        )

        url = f'rtsp://{self.__link["static"]["ip"]}{port}/h264Preview_{(channel+1):02}_{stream.name.lower()}'
        # if isinstance(self, security.Security) and self._auth_token != "":
        #    return f"{url}&token={self._auth_token}"
        return url

    async def get_rtmp_url(
        self, channel: int = 0, stream: IntStreamTypes = IntStreamTypes.MAIN
    ):
        """Get RTMP Url"""

        await self._ensure_ports_and_link()

        port = (
            f':{self.__ports["rtmpPort"]}'
            if self.__ports["rtmpPort"] not in (0, 1935)
            else ""
        )

        url = f'rtmp://{self.__link["static"]["ip"]}{port}/bcs/channel{channel}_{stream.name.lower()}.bcs?channel={channel}&stream={stream}'
        if isinstance(self, security.Security):
            if self._auth_token != "":
                return f"{url}&token={self._auth_token}"
        return url

    async def get_p2p(self):
        """Get P2P"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(GetP2PCommand())
        else:
            return None

        return next(map(GetP2PCommand.get_response, filter(GetP2PCommand.is_response, responses)), None)


class GetLocalLinkResponseValueType(TypedDict):
    """Get Local Link Response Value"""

    LocalLink: LinkInfoType


class GetLocalLinkCommand(CommandRequest):
    """Get Local Link"""

    COMMAND: Final = "GetLocalLink"
    RESPONSE: Final = "LocalLink"

    def __init__(self, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY) -> None:
        super().__init__(type(self).COMMAND, action)

    @classmethod
    def is_response(cls, value: any) -> TypeGuard[GetLocalLinkResponseValueType]:  # pylint: disable=arguments-differ
        """Is response a search result"""
        return (
            super().is_response(value, command=cls.COMMAND)
            and super()._is_typed_value(value, cls.RESPONSE, GetLocalLinkResponseValueType)
        )

    @classmethod
    def get_response(cls, value: GetLocalLinkResponseValueType):
        """Get Local Link Response"""
        return value[cls.RESPONSE]


class GetChannelStatusResponseValueType(TypedDict):
    """Get Channel Status Response Value"""

    count: int
    status: list[ChannelStatusType]


class GetChannelStatusCommand(CommandRequest):
    """Get Channel Status"""

    COMMAND: Final = "GetChannelstatus"
    RESPONSE: Final = "status"

    def __init__(self, action=CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action)

    @classmethod
    def is_response(cls, value: any) -> TypeGuard[GetChannelStatusResponseValueType]:  # pylint: disable=arguments-differ
        """Is response a Channel Status result"""
        return (
            super().is_response(value, command=cls.COMMAND)
            and super()._is_typed_value(value, cls.RESPONSE, GetChannelStatusResponseValueType)
        )

    @classmethod
    def get_response(cls, value: GetChannelStatusResponseValueType):
        """Get Channel Status Response"""
        return value[cls.RESPONSE]


class GetRTSPUrlCommandResponseValueType(TypedDict):
    """Get RTSP Command Response Value"""

    rtspUrl: RTSPUrlsType


class GetRTSPUrlsCommand(CommandRequest):
    """Get RTSP URls"""

    COMMAND: Final = "GetRtspUrl"
    RESPONSE: Final = "rtspUrl"

    def __init__(self, action=CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action)

    @classmethod
    def is_response(cls, value: any) -> TypeGuard[GetRTSPUrlCommandResponseValueType]:  # pylint: disable=arguments-differ
        """Is response a RSTP Url result"""
        return (
            super().is_response(value, command=cls.COMMAND)
            and super()._is_typed_value(value, cls.RESPONSE, GetRTSPUrlCommandResponseValueType)
        )

    @classmethod
    def get_response(cls, value: GetRTSPUrlCommandResponseValueType):
        """Get RSTP Url Response"""
        return value[cls.RESPONSE]


class GetNetworkPortsCommandResponseValueType(TypedDict):
    """Get Network Ports Command Response Value"""

    NetPort: NetworkPortsType


class GetNetworkPortsCommand(CommandRequest):
    """Get Network Ports"""

    COMMAND: Final = "GetNetPort"
    RESPONSE: Final = "NetPort"

    def __init__(self, action=CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action)

    @classmethod
    def is_response(cls, value: any) -> TypeGuard[GetNetworkPortsCommandResponseValueType]:  # pylint: disable=arguments-differ
        """Is response a Network Port result"""
        return (
            super().is_response(value, command=cls.COMMAND)
            and super()._is_typed_value(value, cls.RESPONSE, GetNetworkPortsCommandResponseValueType)
        )

    @classmethod
    def get_response(cls, value: GetNetworkPortsCommandResponseValueType):
        """Get Network Port Response"""
        return value[cls.RESPONSE]


class GetP2PResponseValueType(TypedDict):
    """Get P2P Response Value"""

    P2p: P2PInfoType


class GetP2PCommand(CommandRequest):
    """Get P2P"""

    COMMAND: Final = "GetP2p"
    RESPONSE: Final = "P2p"

    def __init__(self, action=CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action)

    @classmethod
    def is_response(cls, value: any) -> TypeGuard[GetP2PResponseValueType]:  # pylint: disable=arguments-differ
        """Is response a P2P result"""
        return (
            super().is_response(value, command=cls.COMMAND)
            and super()._is_typed_value(value, cls.RESPONSE, GetP2PResponseValueType)
        )

    @classmethod
    def get_response(cls, value: GetP2PResponseValueType):
        """Get P2P Response"""
        return value[cls.RESPONSE]
