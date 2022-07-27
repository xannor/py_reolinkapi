"""Network 3.3"""
from __future__ import annotations

from typing import TYPE_CHECKING, Final, TypedDict, cast, TypeGuard

from backports.strenum import StrEnum

from .utils import afilter, amap

from .commands import (
    CommandRequest,
    CommandRequestTypes,
    CommandResponseValue,
    async_trap_errors,
)

from .const import IntStreamTypes

from . import connection, system, security


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

        Command = GetLocalLinkCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(Command()))
        else:
            return None

        result = await anext(
            amap(Command.get_value, afilter(Command.is_response, responses)),
            None,
        )

        self.__link = result
        return result

    async def get_channel_status(self):
        """Get Channel Statuses Link"""

        Command = GetChannelStatusCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(Command()))
        else:
            return []

        result = await anext(
            amap(Command.get_value, afilter(Command.is_response, responses)),
            None,
        )

        return result or []

    async def get_ports(self):
        """Get Network Ports Url"""

        self.__ports = None
        Command = GetNetworkPortsCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(Command()))
        else:
            return None

        result = await anext(
            amap(Command.get_value, afilter(Command.is_response, responses)),
            None,
        )

        self.__ports = result
        return result

    async def _ensure_ports_and_link(self):

        commands = []
        if self.__link is None:
            if isinstance(self, system.System):
                abilities = await self._ensure_abilities()
                if abilities.localLink:
                    commands.append(GetLocalLinkCommand())
            else:
                commands.append(GetLocalLinkCommand())
        if self.__ports is None:
            commands.append(GetNetworkPortsCommand())

        if not commands:
            return
        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(*commands))
        else:
            return

        async for response in responses:
            if GetLocalLinkCommand.is_response(response):
                self.__link = GetLocalLinkCommand.get_value(response)
            if GetNetworkPortsCommand.is_response(response):
                self.__ports = GetNetworkPortsCommand.get_value(response)

    async def get_rtsp_url(
        self, channel: int = 0, stream: IntStreamTypes = IntStreamTypes.MAIN
    ):
        """Get RTSP Url"""

        if not self.__no_get_rtsp:
            if isinstance(self, system.System):
                abilities = await self._ensure_abilities()
                if abilities.scheduleVersion == system.abilities.VersionValues.BASIC:
                    self.__no_get_rtsp = True

        if not self.__no_get_rtsp:

            def _ignore_errors(*_):
                return True

            Command = GetRTSPUrlsCommand

            if isinstance(self, connection.Connection):
                responses = async_trap_errors(
                    self._execute(Command(), _ignore_errors))

                result = await anext(
                    amap(Command.get_value, afilter(
                        Command.is_response, responses)),
                    None,
                )

                if result:
                    url = result[f"{stream.name.lower()}Stream"]
                    if TYPE_CHECKING:
                        url = cast(str, url)
                    return url

            self.__no_get_rtsp = True

        await self._ensure_ports_and_link()

        port = (
            f':{self.__ports["rtspPort"]}'
            if self.__ports["rtspPort"] not in (0, 554)
            else ""
        )

        url = f'rtsp://{self.__link["static"]["ip"]}{port}/h264Preview_{(channel+1):02}_{stream.name.lower()}'
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

        Command = GetP2PCommand

        if isinstance(self, connection.Connection):
            responses = async_trap_errors(self._execute(Command()))
        else:
            return None

        result = await anext(
            amap(Command.get_value, afilter(Command.is_response, responses)),
            None,
        )

        return result


class GetLocalLinkResponseValueType(TypedDict):
    """Get Local Link Response Value"""

    LocalLink: LinkInfoType


class GetLocalLinkCommand(CommandRequest):
    """Get Local Link"""

    COMMAND: Final = "GetLocalLink"
    RESPONSE: Final = "LocalLink"

    def __init__(
        self, action: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY
    ) -> None:
        super().__init__(type(self).COMMAND, action)

    @classmethod
    def is_response(  # pylint: disable=arguments-differ
        cls, value: any
    ) -> TypeGuard[CommandResponseValue[GetLocalLinkResponseValueType]]:
        """Is response a search result"""
        return super().is_response(
            value, command=cls.COMMAND
        ) and super()._is_typed_value(
            value, cls.RESPONSE, GetLocalLinkResponseValueType
        )

    @classmethod
    def get_value(cls, value: CommandResponseValue[GetLocalLinkResponseValueType]):
        """Get Response Value"""
        return cls._get_value(value)[  # pylint: disable=unsubscriptable-object
            cls.RESPONSE
        ]


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
    def is_response(  # pylint: disable=arguments-differ
        cls, value: any
    ) -> TypeGuard[CommandResponseValue[GetChannelStatusResponseValueType]]:
        """Is response a Channel Status result"""
        return super().is_response(
            value, command=cls.COMMAND
        ) and super()._is_typed_value(
            value, cls.RESPONSE, GetChannelStatusResponseValueType
        )

    @classmethod
    def get_value(cls, value: CommandResponseValue[GetChannelStatusResponseValueType]):
        """Get Response Value"""
        return cls._get_value(value)[  # pylint: disable=unsubscriptable-object
            cls.RESPONSE
        ]


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
    def is_response(  # pylint: disable=arguments-differ
        cls, value: any
    ) -> TypeGuard[CommandResponseValue[GetRTSPUrlCommandResponseValueType]]:
        """Is response a RSTP Url result"""
        return super().is_response(
            value, command=cls.COMMAND
        ) and super()._is_typed_value(
            value, cls.RESPONSE, GetRTSPUrlCommandResponseValueType
        )

    @classmethod
    def get_value(cls, value: CommandResponseValue[GetRTSPUrlCommandResponseValueType]):
        """Get Response Value"""
        return cls._get_value(value)[  # pylint: disable=unsubscriptable-object
            cls.RESPONSE
        ]


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
    def is_response(  # pylint: disable=arguments-differ
        cls, value: any
    ) -> TypeGuard[CommandResponseValue[GetNetworkPortsCommandResponseValueType]]:
        """Is response a Network Port result"""
        return super().is_response(
            value, command=cls.COMMAND
        ) and super()._is_typed_value(
            value, cls.RESPONSE, GetNetworkPortsCommandResponseValueType
        )

    @classmethod
    def get_value(
        cls, value: CommandResponseValue[GetNetworkPortsCommandResponseValueType]
    ):
        """Get Response Value"""
        return cls._get_value(value)[  # pylint: disable=unsubscriptable-object
            cls.RESPONSE
        ]


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
    def is_response(  # pylint: disable=arguments-differ
        cls, value: any
    ) -> TypeGuard[CommandResponseValue[GetP2PResponseValueType]]:
        """Is response a P2P result"""
        return super().is_response(
            value, command=cls.COMMAND
        ) and super()._is_typed_value(value, cls.RESPONSE, GetP2PResponseValueType)

    @classmethod
    def get_value(cls, value: CommandResponseValue[GetP2PResponseValueType]):
        """Get Response Value"""
        return cls._get_value(value)[  # pylint: disable=unsubscriptable-object
            cls.RESPONSE
        ]
