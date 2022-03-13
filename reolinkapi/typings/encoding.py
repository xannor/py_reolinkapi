"""Encoding Typings"""

from typing import TypedDict


class StreamEncodingInfo(TypedDict):
    """Encoding Info"""

    bitRate: int
    frameRate: int
    gop: int
    height: int
    width: int
    profile: str
    size: str
    vType: str


class EncodingInfo(TypedDict):
    """Encoding Info"""

    audio: bool
    channel: int
    mainStream: StreamEncodingInfo
    subStream: StreamEncodingInfo
    extStream: StreamEncodingInfo
