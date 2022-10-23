"""Network Commands"""

from typing import Mapping, Protocol, TypeGuard

from ..connection.typing import ChannelValue
from ..connection.typing import CommandFactory as WithCommandFactory
from ..connection.typing import CommandRequest, CommandResponse
from ..typing import StreamTypes
from .typing import ChannelStatus, LinkInfo, NetworkPorts, P2PInfo, WifiInfo


class GetLocalLinkRequest(CommandRequest, Protocol):
    """Get Local Link Request"""


class GetLocalLinkResponse(CommandResponse, Protocol):
    """Get Local Link Response"""

    local_link: LinkInfo


class GetChannelStatusRequest(CommandRequest, Protocol):
    """Get Channel Status Request"""


class GetChannelStatusResponse(CommandResponse, Protocol):
    """Get Channel Status Response"""

    channels: Mapping[int, ChannelStatus]


class GetNetworkPortsRequest(CommandRequest, Protocol):
    """Get Network Ports Request"""


class GetNetworkPortsResponse(CommandResponse, Protocol):
    """Get Network Ports Response"""

    ports: NetworkPorts


class GetRTSPUrlsRequest(CommandRequest, ChannelValue, Protocol):
    """Get RTSP URls Request"""


class GetRTSPUrlsResponse(CommandResponse, ChannelValue, Protocol):
    """Get RTSP Urls Repsonse"""

    urls: Mapping[StreamTypes, str]


class GetP2PRequest(CommandRequest, Protocol):
    """Get P2P Info Request"""


class GetP2PResponse(CommandResponse, Protocol):
    """Get P2P Info Response"""

    info: P2PInfo


class GetWifiInfoRequest(CommandRequest, Protocol):
    """Get Wifi Info Request"""


class GetWifiInfoResponse(CommandResponse, Protocol):
    """Get Wifi Info Response"""

    info: WifiInfo


class GetWifiSignalRequest(CommandRequest, Protocol):
    """Get Wifi Signal Strength Request"""


class GetWifiSignalResponse(CommandRequest, Protocol):
    """Get Wifi Signal Stength Response"""

    signal: int


class CommandFactory(WithCommandFactory, Protocol):
    """Network Command Factory"""

    def create_get_local_link_request(self) -> GetLocalLinkRequest:
        """create GetLocalLinkRequest"""

    def is_get_local_link_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetLocalLinkResponse]:
        """is GetLocalLinkResponse"""

    def create_get_channel_status_request(self) -> GetChannelStatusRequest:
        """create GetChannelStatusRequest"""

    def is_get_channel_status_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetChannelStatusResponse]:
        """is GetChannelStatusResponse"""

    def create_get_ports_request(self) -> GetNetworkPortsRequest:
        """create GetNetworkPortsRequest"""

    def is_get_ports_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetNetworkPortsResponse]:
        """is GetNetworkPortsResponse"""

    def create_get_rtsp_urls_request(self, channel_id: int) -> GetRTSPUrlsRequest:
        """create GetRTSPUrlsRequest"""

    def is_get_rtsp_urls_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetRTSPUrlsResponse]:
        """is GetRTSPUrlsResponse"""

    def create_get_p2p_request(self) -> GetP2PRequest:
        """create GetP2PRequest"""

    def is_get_p2p_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetP2PResponse]:
        """is GetP2PResponse"""

    def create_get_wifi_info_request(self) -> GetWifiInfoRequest:
        """create GetWifiInfoRequest"""

    def is_get_wifi_info_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetWifiInfoResponse]:
        """is GetWifiInfoResponse"""

    def create_get_wifi_signal_request(self) -> GetWifiSignalRequest:
        """create GetWifiSignalRequest"""

    def is_get_wifi_signal_response(
        self, response: CommandResponse
    ) -> TypeGuard[GetWifiSignalResponse]:
        """is GetWifiSignalResponse"""
