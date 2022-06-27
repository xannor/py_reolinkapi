"""Network 3.3"""

from dataclasses import dataclass
from enum import Enum
from typing import Final, TypedDict

from pyparsing import Iterable

from .commands import COMMAND_RESPONSE_VALUE, CommandRequest, CommandRequestTypes, CommandRequestWithParam, CommandResponse, create_is_command, create_value_has_key, isvalue

from .const import StreamTypes

from . import connection, security

class LinkType(Enum):
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
            responses = await self._execute(GetLocalLinkRequest())
        else:
            return None

        link = next(GetLocalLinkRequest.get_responses(responses), None)
        if link is not None:
            self.__link = link
        return link

    async def get_channel_status(self):
        """Get Channel Statuses Link"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(GetChannelStatusRequest())
        else:
            return None

        status = next(GetChannelStatusRequest.get_responses(responses), None)
        if status is not None:
            return status["status"]

    async def get_ports(self):
        """Get Network Ports Url"""

        self.__ports = None
        if isinstance(self, connection.Connection):
            responses = await self._execute(GetNetworkPortsRequest())
        else:
            return None

        ports = next(GetNetworkPortsRequest.get_responses(responses), None)
        if ports is not None:
            self.__ports = ports
        return ports

    async def _ensure_ports_and_link(self):
        commands = []
        if self.__link is None:
            commands.append(GetLocalLinkRequest())
        if self.__ports is None:
            commands.append(GetNetworkPortsRequest())

        if len(commands) > 0 and isinstance(self, connection.Connection):
            responses = await self._execute(*commands)
        else:
            responses = []

        link = next(GetLocalLinkRequest.get_responses(responses), None)
        ports = next(GetNetworkPortsRequest.get_responses(responses), None)
        if link is not None:
            self.__link = link
        if ports is not None:
            self.__ports = ports

    async def get_rtsp_url(
        self, channel: int = 0, stream: StreamTypes = StreamTypes.MAIN
    ):
        """Get RTSP Url"""

        if not self.__no_get_rtsp:
            responses = None
            if isinstance(self, connection.Connection):
                responses = await self._execute(GetRTSPUrlsRequest())

            if responses is not None:
                urls = next(GetRTSPUrlsRequest.get_responses(responses), None)
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
        self, channel: int = 0, stream: StreamTypes = StreamTypes.MAIN
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
            responses = await self._execute(GetP2PRequest())
        else:
            return None

        return next(GetP2PRequest.get_responses(responses), None)

class GetLocalLinkResponseValue(TypedDict):
    """Get Local Link Response Value"""

    LocalLink: LinkInfoType

class GetLocalLinkRequest(CommandRequest):
    """Get Local Link"""

    COMMAND:Final = "GetLocalLink"
    RESPONSE:Final = "LocalLink"

    def __init__(self, action:CommandRequestTypes=CommandRequestTypes.VALUE_ONLY)->None:
        super().__init__(type(self).COMMAND, action)

    @classmethod
    def get_responses(cls, responses: Iterable[CommandResponse]):
        """"Get Responses"""
        return map(
            lambda response: response[COMMAND_RESPONSE_VALUE][cls.RESPONSE],
            filter(
                _isLocalLink,
                filter(
                    isvalue,
                    filter(
                        _isLocalLinkCmd,
                        responses
                    )
                )
            )
        )


_isLocalLinkCmd = create_is_command(GetLocalLinkRequest.COMMAND)

_isLocalLink = create_value_has_key(
    GetLocalLinkRequest.RESPONSE, GetLocalLinkResponseValue
)


class GetChannelStatusResponseValue(TypedDict):
    """Get Channel Status Response Value"""

    count: int
    status: list[ChannelStatusType]


class GetChannelStatusRequest(CommandRequest):
    """Get Channel Status"""

    COMMAND:Final = "GetChannelstatus"
    RESPONSE:Final = "status"

    def __init__(self, action=CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action)

    @classmethod
    def get_responses(cls, responses:Iterable[CommandResponse]):
        """ Get ChannelStatus[] Responses"""
        return map(
            lambda response: response[COMMAND_RESPONSE_VALUE],
            filter(
                _isChannelStatus,
                filter(
                    isvalue,
                    filter(
                        _isChannelStatusCmd,
                        responses,
                    ),
                ),
            ),
        )


_isChannelStatusCmd = create_is_command(GetChannelStatusRequest.COMMAND)

_isChannelStatus = create_value_has_key(
    GetChannelStatusRequest.RESPONSE, GetChannelStatusResponseValue, list
)

class GetRTSPUrlCommandResponseValue(TypedDict):
    """Get RTSP Command Response Value"""

    rtspUrl: RTSPUrlsType

class GetRTSPUrlsRequest(CommandRequest):
    """Get RTSP URls"""

    COMMAND: Final = "GetRtspUrl"
    RESPONSE: Final = "rtspUrl"

    def __init__(self, action=CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action)

    @classmethod
    def get_responses(cls, responses:Iterable[CommandResponse]):
        """ Get RTSP Urls Responses"""
        return map(
            lambda response: response[COMMAND_RESPONSE_VALUE][cls.RESPONSE],
            filter(
                _isRTSPUrl,
                filter(
                    isvalue,
                    filter(
                        _isRTSPUrlCmd,
                        responses,
                    ),
                ),
            ),
        )


_isRTSPUrlCmd = create_is_command(GetRTSPUrlsRequest.COMMAND)

_isRTSPUrl = create_value_has_key(
    GetRTSPUrlsRequest.RESPONSE, GetRTSPUrlCommandResponseValue
)


class GetNetworkPortsCommandResponseValue(TypedDict):
    """Get Network Ports Command Response Value"""

    NetPort: NetworkPortsType

class GetNetworkPortsRequest(CommandRequest):
    """Get Network Ports"""

    COMMAND: Final = "GetNetPort"
    RESPONSE: Final = "NetPort"

    def __init__(self, action=CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action)

    @classmethod
    def get_responses(cls, responses:Iterable[CommandResponse]):
        """ Get Network Ports Responses"""
        return map(
            lambda response: response[COMMAND_RESPONSE_VALUE][cls.RESPONSE],
            filter(
                _isNetworkPorts,
                filter(
                    isvalue,
                    filter(
                        _isNetworkPortsCmd,
                        responses,
                    ),
                ),
            ),
        )

_isNetworkPortsCmd = create_is_command(GetNetworkPortsRequest.COMMAND)

_isNetworkPorts = create_value_has_key(
    GetNetworkPortsRequest.RESPONSE, GetNetworkPortsCommandResponseValue
)

class GetP2PResponseValue(TypedDict):
    """Get P2P Response Value"""

    P2p: P2PInfoType

class GetP2PRequest(CommandRequest):
    """Get P2P"""

    COMMAND: Final = "GetP2p"
    RESPONSE:Final = "P2p"

    def __init__(self, action=CommandRequestTypes.VALUE_ONLY):
        super().__init__(type(self).COMMAND, action)

    @classmethod
    def get_responses(cls, responses:Iterable[CommandResponse]):
        """ Get Network Ports Responses"""
        return map(
            lambda response: response[COMMAND_RESPONSE_VALUE][cls.RESPONSE],
            filter(
                _isP2P,
                filter(
                    isvalue,
                    filter(
                        _isP2PCmd,
                        responses,
                    ),
                ),
            ),
        )

_isP2PCmd = create_is_command(GetP2PRequest.COMMAND)

_isP2P = create_value_has_key(GetP2PRequest.RESPONSE, GetP2PResponseValue)
