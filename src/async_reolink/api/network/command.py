"""Network Commands"""

from typing import Mapping, Protocol

from ..connection.typing import ChannelValue
from ..typing import StreamTypes
from .typing import ChannelStatus, LinkInfo, NetworkPorts, P2PInfo, WifiInfo


class GetLocalLinkRequest(Protocol):
    """Get Local Link Request"""


class GetLocalLinkResponse(Protocol):
    """Get Local Link Response"""

    local_link: LinkInfo


class GetChannelStatusRequest(Protocol):
    """Get Channel Status Request"""


class GetChannelStatusResponse(Protocol):
    """Get Channel Status Response"""

    channels: Mapping[int, ChannelStatus]


class GetNetworkPortsRequest(Protocol):
    """Get Network Ports Request"""


class GetNetworkPortsResponse(Protocol):
    """Get Network Ports Response"""

    ports: NetworkPorts


class GetRTSPUrlsRequest(ChannelValue, Protocol):
    """Get RTSP URls Request"""


class GetRTSPUrlsResponse(ChannelValue, Protocol):
    """Get RTSP Urls Repsonse"""

    urls: Mapping[StreamTypes, str]


class GetP2PRequest(Protocol):
    """Get P2P Info Request"""


class GetP2PResponse(Protocol):
    """Get P2P Info Response"""

    info: P2PInfo


class GetWifiInfoRequest(Protocol):
    """Get Wifi Info Request"""


class GetWifiInfoResponse(Protocol):
    """Get Wifi Info Response"""

    info: WifiInfo


class GetWifiSignalRequest(Protocol):
    """Get Wifi Signal Strength Request"""


class GetWifiSignalResponse(Protocol):
    """Get Wifi Signal Stength Response"""

    signal: int
