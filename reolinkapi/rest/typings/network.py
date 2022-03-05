"""Network Commands"""
from __future__ import annotations

from enum import Enum
from typing import TypedDict


class LinkType(Enum):
    """Link Type"""

    STATIC = "Static"
    DHCP = "DHCP"


class IPInfo(TypedDict):
    """IP Information"""

    gateway: str
    ip: str
    mask: str


class LinkInfo(TypedDict):
    """Link Information"""

    activeLink: str
    mac: str
    type: str
    static: IPInfo


class ChannelStatus(TypedDict):
    """Channel Status"""

    channel: int
    name: str
    online: bool
    typeInfo: str


class RTSPUrls(TypedDict):
    """RTSP Url Info"""

    channel: int
    mainStream: str
    subStream: str
    extStream: str


class NetworkPorts(TypedDict):
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
