"""Network Helpers"""

from typing import Final, Iterable, TypedDict

from ..typings.commands import (
    COMMAND_RESPONSE_VALUE,
    CommandRequest,
    CommandRequestTypes,
    CommandRequestWithParam,
    CommandResponse,
)
from ..typings.network import ChannelStatus, LinkInfo, NetworkPorts, P2PInfo, RTSPUrls

from ..helpers import commands as commandHelpers


class GetLocalLinkResponseValue(TypedDict):
    """Get Local Link Response Value"""

    LocalLink: LinkInfo


GET_LOCAL_LINK_COMMAND: Final = "GetLocalLink"

_isLocalLinkCmd = commandHelpers.create_is_command(GET_LOCAL_LINK_COMMAND)

_isLocalLink = commandHelpers.create_value_has_key(
    "LocalLink", GetLocalLinkResponseValue
)


def create_get_local_link(
    _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
):
    """Create LocalLink Request"""
    return CommandRequestWithParam(cmd=GET_LOCAL_LINK_COMMAND, action=_type)


def get_local_link_responses(responses: Iterable[CommandResponse]):
    """Get LocalLink Responses"""
    return map(
        lambda response: response[COMMAND_RESPONSE_VALUE]["LocalLink"],
        filter(
            _isLocalLink,
            filter(
                commandHelpers.isvalue,
                filter(
                    _isLocalLinkCmd,
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

_isChannelStatusCmd = commandHelpers.create_is_command(GET_CHANNEL_STATUS_COMMAND)

_isChannelStatus = commandHelpers.create_value_has_key(
    "status", GetChannelStatusResponseValue, list
)


def create_get_channel_status(
    _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
):
    """Create GetChannelStatus Request"""
    return CommandRequestWithParam(cmd=GET_CHANNEL_STATUS_COMMAND, action=_type)


def get_channel_status_responses(responses: Iterable[CommandResponse]):
    """Get ChannelStatus[] Responses"""
    return map(
        lambda response: response[COMMAND_RESPONSE_VALUE],
        filter(
            _isChannelStatus,
            filter(
                commandHelpers.isvalue,
                filter(
                    _isChannelStatusCmd,
                    responses,
                ),
            ),
        ),
    )


class GetRTSPUrlCommandResponseValue(TypedDict):
    """Get RTSP Command Response Value"""

    rtspUrl: RTSPUrls


GET_RTSP_URL_COMMAND: Final = "GetRtspUrl"

_isRTSPUrlCmd = commandHelpers.create_is_command(GET_RTSP_URL_COMMAND)

_isRTSPUrl = commandHelpers.create_value_has_key(
    "rtspUrl", GetRTSPUrlCommandResponseValue
)


def create_get_rtsp_url(
    _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
):
    """Create Get RTSP Url Request"""
    return CommandRequest(cmd=GET_RTSP_URL_COMMAND, action=_type)


def get_rtsp_url_responses(responses: Iterable[CommandResponse]):
    """Get RTSP Urls from responses"""

    return map(
        lambda response: response[COMMAND_RESPONSE_VALUE]["rtspUrl"],
        filter(
            _isRTSPUrl,
            filter(
                commandHelpers.isvalue,
                filter(
                    _isRTSPUrlCmd,
                    responses,
                ),
            ),
        ),
    )


class GetNetworkPortsCommandResponseValue(TypedDict):
    """Get Network Ports Command Response Value"""

    NetPort: NetworkPorts


GET_NETWORK_PORT_COMMAND: Final = "GetNetPort"

_isNetworkPortsCmd = commandHelpers.create_is_command(GET_NETWORK_PORT_COMMAND)

_isNetworkPorts = commandHelpers.create_value_has_key(
    "NetPort", GetNetworkPortsCommandResponseValue
)


def create_get_network_ports(
    _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
):
    """Create GetNetworkProts Request"""
    return CommandRequestWithParam(cmd=GET_NETWORK_PORT_COMMAND, action=_type)


def get_network_ports_responses(responses: Iterable[CommandResponse]):
    """Get NetworkPorts Responses"""
    return map(
        lambda response: response[COMMAND_RESPONSE_VALUE]["NetPort"],
        filter(
            _isNetworkPorts,
            filter(
                commandHelpers.isvalue,
                filter(
                    _isNetworkPortsCmd,
                    responses,
                ),
            ),
        ),
    )


class GetP2PResponseValue(TypedDict):
    """Get P2P Response Value"""

    P2p: P2PInfo


GET_P2P_COMMAND: Final = "GetP2p"

_isP2PCmd = commandHelpers.create_is_command(GET_P2P_COMMAND)

_isP2P = commandHelpers.create_value_has_key("P2p", GetP2PResponseValue)


def create_get_p2p(
    _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
):
    """Create LocalLink Request"""
    return CommandRequest(cmd=GET_P2P_COMMAND, action=_type)


def get_p2p_responses(responses: Iterable[CommandResponse]):
    """Get LocalLink Responses"""
    return map(
        lambda response: response[COMMAND_RESPONSE_VALUE]["P2p"],
        filter(
            _isP2P,
            filter(
                commandHelpers.isvalue,
                filter(
                    _isP2PCmd,
                    responses,
                ),
            ),
        ),
    )
