"""Network Mixin"""
from __future__ import annotations


from typing import Iterable, TypedDict
from urllib.parse import quote_plus

from . import connection, security

from .typings.commands import (
    CommandRequest,
    CommandRequestTypes,
    CommandResponse,
    filter_command_responses,
)
from .typings.network import ChannelStatus, LinkInfo, NetworkPorts, P2PInfo, RTSPUrls

from .const import StreamTypes


class GetLocalLinkResponseValue(TypedDict):
    """Get Local Link Response Value"""

    LocalLink: LinkInfo


def _cast_local_link_response_value(responses: Iterable[CommandResponse]):
    def _cast(response: CommandResponse):
        value: GetLocalLinkResponseValue = response["value"]
        return value["LocalLink"]

    return map(_cast, responses)


GET_LOCAL_LINK_COMMAND = "GetLocalLink"


class GetChannelStatusResponseValue(TypedDict):
    """Get Channel Status Response Value"""

    count: int
    status: list[ChannelStatus]


def _cast_channel_status_response_value(responses: Iterable[CommandResponse]):
    def _cast(response: CommandResponse):
        value: GetChannelStatusResponseValue = response["value"]
        return value

    return map(_cast, responses)


GET_CHANNEL_STATUS_COMMAND = "GetChannelstatus"


class GetRTSPUrlCommandResponseValue(TypedDict):
    """Get RTSP Command Response Value"""

    rtspUrl: RTSPUrls


def _cast_rtsp_url_response_value(responses: Iterable[CommandResponse]):
    def _cast(response: CommandResponse):
        value: GetRTSPUrlCommandResponseValue = response["value"]
        return value["rtspUrl"]

    return map(_cast, responses)


GET_RTSP_URL_COMMAND = "GetRtspUrl"


class GetNetworkPortsCommandResponseValue(TypedDict):
    """Get Network Ports Command Response Value"""

    NetPort: NetworkPorts


def _cast_network_ports_response_value(responses: Iterable[CommandResponse]):
    def _cast(response: CommandResponse):
        value: GetNetworkPortsCommandResponseValue = response["value"]
        return value["NetPort"]

    return map(_cast, responses)


class GetP2PResponseValue(TypedDict):
    """Get P2P Response Value"""

    P2p: P2PInfo


def _cast_p2p_response_value(responses: Iterable[CommandResponse]):
    def _cast(response: CommandResponse):
        value: GetP2PResponseValue = response["value"]
        return value["P2p"]

    return map(_cast, responses)


GET_P2P_COMMAND = "GetP2p"


GET_NETWORK_PORT_COMMAND = "GetNetPort"


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
        return CommandRequest(cmd=GET_LOCAL_LINK_COMMAND, action=_type)

    @staticmethod
    def get_local_link_responses(responses: Iterable[CommandResponse]):
        """Get LocalLink Responses"""

        return _cast_local_link_response_value(
            filter_command_responses(GET_LOCAL_LINK_COMMAND, responses)
        )

    async def get_local_link(self):
        """Get Local Link"""

        self.__link = None
        link = next(
            _cast_local_link_response_value(
                filter_command_responses(
                    GET_LOCAL_LINK_COMMAND,
                    await self._execute(Network.create_get_local_link()),
                )
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
        return CommandRequest(cmd=GET_CHANNEL_STATUS_COMMAND, action=_type)

    @staticmethod
    def get_channel_status_responses(responses: Iterable[CommandResponse]):
        """Get ChannelStatus[] Responses"""

        return _cast_channel_status_response_value(
            filter_command_responses(GET_CHANNEL_STATUS_COMMAND, responses)
        )

    async def get_channel_status(self):
        """Get Channel Statuses Link"""

        status = next(
            _cast_channel_status_response_value(
                filter_command_responses(
                    GET_CHANNEL_STATUS_COMMAND,
                    await self._execute(Network.create_get_channel_status()),
                )
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
        return CommandRequest(cmd=GET_NETWORK_PORT_COMMAND, action=_type)

    @staticmethod
    def get_network_ports_responses(responses: Iterable[CommandResponse]):
        """Get NetworkPorts Responses"""

        return _cast_network_ports_response_value(
            filter_command_responses(GET_NETWORK_PORT_COMMAND, responses)
        )

    async def get_ports(self):
        """Get Network Ports Url"""

        self.__ports = None
        ports = next(
            _cast_network_ports_response_value(
                filter_command_responses(
                    GET_NETWORK_PORT_COMMAND,
                    await self._execute(Network.create_get_network_ports()),
                )
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
        return CommandRequest(cmd=GET_P2P_COMMAND, action=_type)

    @staticmethod
    def get_p2p_responses(responses: Iterable[CommandResponse]):
        """Get LocalLink Responses"""

        return _cast_p2p_response_value(
            filter_command_responses(GET_P2P_COMMAND, responses)
        )

    async def get_p2p(self):
        """Get P2P"""

        return next(
            _cast_p2p_response_value(
                filter_command_responses(
                    GET_P2P_COMMAND,
                    await self._execute(Network.create_get_p2p()),
                )
            ),
            None,
        )
