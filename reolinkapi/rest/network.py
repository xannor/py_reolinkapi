"""Network Mixin"""
from __future__ import annotations


from typing import Final, Iterable, TypedDict
from urllib.parse import quote_plus

from . import connection, security

from ..typings.commands import (
    CommandRequestWithParam,
    CommandRequestTypes,
    CommandResponse,
)
from ..typings.network import ChannelStatus, LinkInfo, NetworkPorts, P2PInfo, RTSPUrls

from .const import StreamTypes
from ..helpers import commands as commandHelpers


class GetLocalLinkResponseValue(TypedDict):
    """Get Local Link Response Value"""

    LocalLink: LinkInfo


GET_LOCAL_LINK_COMMAND: Final = "GetLocalLink"

_isLocalLink = commandHelpers.create_value_has_key(
    "LocalLink", GetLocalLinkResponseValue
)


def _get_local_link_responses(responses: Iterable[CommandResponse]):
    return map(
        lambda response: response["value"]["LocalLink"],
        filter(
            _isLocalLink,
            filter(
                commandHelpers.isvalue,
                filter(
                    lambda response: response["cmd"] == GET_LOCAL_LINK_COMMAND,
                    responses,
                ),
            ),
        ),
    )


class GetChannelStatusResponseValue(TypedDict):
    """Get Channel Status Response Value"""

    count: int
    status: list[ChannelStatus]


GET_CHANNEL_STATUS_COMMAND: Final = "GetChannelstatus"

_isChannelStatus = commandHelpers.create_value_has_key(
    "status", GetChannelStatusResponseValue, list
)


def _get_channel_status_responses(responses: Iterable[CommandResponse]):
    return map(
        lambda response: response["value"],
        filter(
            _isChannelStatus,
            filter(
                commandHelpers.isvalue,
                filter(
                    lambda response: response["cmd"] == GET_CHANNEL_STATUS_COMMAND,
                    responses,
                ),
            ),
        ),
    )


class GetRTSPUrlCommandResponseValue(TypedDict):
    """Get RTSP Command Response Value"""

    rtspUrl: RTSPUrls


GET_RTSP_URL_COMMAND: Final = "GetRtspUrl"

_isRTSPUrl = commandHelpers.create_value_has_key(
    "rtspUrl", GetRTSPUrlCommandResponseValue
)


def _get_rtsp_url_responses(responses: Iterable[CommandResponse]):
    return map(
        lambda response: response["value"]["rtspUrl"],
        filter(
            _isRTSPUrl,
            filter(
                commandHelpers.isvalue,
                filter(
                    lambda response: response["cmd"] == GET_RTSP_URL_COMMAND,
                    responses,
                ),
            ),
        ),
    )


class GetNetworkPortsCommandResponseValue(TypedDict):
    """Get Network Ports Command Response Value"""

    NetPort: NetworkPorts


GET_NETWORK_PORT_COMMAND: Final = "GetNetPort"

_isNetworkPorts = commandHelpers.create_value_has_key(
    "NetPort", GetNetworkPortsCommandResponseValue
)


def _get_network_port_responses(responses: Iterable[CommandResponse]):
    return map(
        lambda response: response["value"]["NetPort"],
        filter(
            _isNetworkPorts,
            filter(
                commandHelpers.isvalue,
                filter(
                    lambda response: response["cmd"] == GET_NETWORK_PORT_COMMAND,
                    responses,
                ),
            ),
        ),
    )


class GetP2PResponseValue(TypedDict):
    """Get P2P Response Value"""

    P2p: P2PInfo


GET_P2P_COMMAND: Final = "GetP2p"

_isP2P = commandHelpers.create_value_has_key("P2p", GetP2PResponseValue)


def _get_p2p_responses(responses: Iterable[CommandResponse]):
    return map(
        lambda response: response["value"]["P2p"],
        filter(
            _isP2P,
            filter(
                commandHelpers.isvalue,
                filter(
                    lambda response: response["cmd"] == GET_P2P_COMMAND,
                    responses,
                ),
            ),
        ),
    )


class Network:
    """Network commands Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__link: LinkInfo | None = None
        self.__ports: NetworkPorts | None = None
        self.__no_get_rtsp = False
        other: any = self
        if isinstance(other, connection.Connection):
            other._disconnect_callbacks.append(self.__clear)
            if not hasattr(self, "_execute"):
                self._execute = other._execute
        if isinstance(other, security.Security) and not hasattr(self, "_auth_token"):
            self._auth_token = other._auth_token

    def __clear(self):
        self.__no_get_rtsp = False
        self.__link = None
        self.__ports = None

    @staticmethod
    def create_get_local_link(
        _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
    ):
        """Create LocalLink Request"""
        return CommandRequestWithParam(cmd=GET_LOCAL_LINK_COMMAND, action=_type)

    @staticmethod
    def get_local_link_responses(responses: Iterable[CommandResponse]):
        """Get LocalLink Responses"""

        return _get_local_link_responses(responses)

    async def get_local_link(self):
        """Get Local Link"""

        self.__link = None
        link = next(
            _get_local_link_responses(
                await self._execute(Network.create_get_local_link())
            ),
            None,
        )
        if link is not None:
            self.__link = link
        return link

    @staticmethod
    def create_get_channel_status(
        _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
    ):
        """Create GetChannelStatus Request"""
        return CommandRequestWithParam(cmd=GET_CHANNEL_STATUS_COMMAND, action=_type)

    @staticmethod
    def get_channel_status_responses(responses: Iterable[CommandResponse]):
        """Get ChannelStatus[] Responses"""

        return _get_channel_status_responses(responses)

    async def get_channel_status(self):
        """Get Channel Statuses Link"""

        status = next(
            _get_channel_status_responses(
                await self._execute(Network.create_get_channel_status()),
            ),
            None,
        )
        if status is not None:
            return status["status"]
        return status

    @staticmethod
    def create_get_network_ports(
        _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
    ):
        """Create GetNetworkProts Request"""
        return CommandRequestWithParam(cmd=GET_NETWORK_PORT_COMMAND, action=_type)

    @staticmethod
    def get_network_ports_responses(responses: Iterable[CommandResponse]):
        """Get NetworkPorts Responses"""

        return _get_network_port_responses(responses)

    async def get_ports(self):
        """Get Network Ports Url"""

        self.__ports = None
        ports = next(
            _get_network_port_responses(
                await self._execute(Network.create_get_network_ports()),
            ),
            None,
        )
        if ports is not None:
            self.__ports = ports
        return ports

    async def _ensure_ports_and_link(self):
        commands = []
        if self.__link is None:
            commands.append(Network.create_get_local_link())
        if self.__ports is None:
            commands.append(Network.create_get_network_ports())

        results = await self._execute(*commands) if len(commands) > 0 else []
        link = next(Network.get_local_link_responses(results))
        ports = next(Network.get_network_ports_responses(results))
        if link is not None:
            self.__link = link
        if ports is not None:
            self.__ports = ports

    async def get_rtsp_url(
        self, channel: int = 0, stream: StreamTypes = StreamTypes.MAIN
    ):
        """Get RTSP Url"""

        if not self.__no_get_rtsp:
            results = await self._execute(
                CommandRequestWithParam(
                    cmd=GET_RTSP_URL_COMMAND, action=CommandRequestTypes.VALUE_ONLY
                )
            )
            if len(results) == 1:
                result = results[0]
                if (
                    commandHelpers.isvalue(result)
                    and result["cmd"] == GET_RTSP_URL_COMMAND
                    and _isRTSPUrl(result)
                ):
                    result = result["value"]["rtspUrl"]
                    url: str = result[f"{stream.name.lower()}Stream"]
                    return url

            self.__no_get_rtsp = True

        await self._ensure_ports_and_link()

        port = (
            f':{self.__ports["rtspPort"]}'
            if self.__ports["rtspPort"] not in (0, 554)
            else ""
        )

        url = f'rtsp://{self.__link["static"]["ip"]}{port}/h264Preview_{channel:02}_{stream.name.lower()}'
        if self._auth_token:
            return f"{url}&Token={quote_plus(self._auth_token)}"
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
        if self._auth_token != "":
            return f"{url}&Token={quote_plus(self._auth_token)}"
        return url

    @staticmethod
    def create_get_p2p(
        _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
    ):
        """Create LocalLink Request"""
        return CommandRequestWithParam(cmd=GET_P2P_COMMAND, action=_type)

    @staticmethod
    def get_p2p_responses(responses: Iterable[CommandResponse]):
        """Get LocalLink Responses"""

        return _get_p2p_responses(responses)

    async def get_p2p(self):
        """Get P2P"""

        return next(
            _get_p2p_responses(
                await self._execute(Network.create_get_p2p()),
            ),
            None,
        )
