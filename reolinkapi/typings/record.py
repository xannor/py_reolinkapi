"""Record Typings"""

from typing import TypedDict

from ..const import STREAM_TYPES
from .system import TimeValue


class Search(TypedDict):
    """Search"""

    channel: int
    onlyStatus: int
    streamType: STREAM_TYPES
    StartTime: TimeValue
    EndTime: TimeValue


class SearchStatus(TypedDict):
    """Search Result Status"""

    mon: int
    year: int
    table: str


class SearchFile(TypedDict):
    """Search Result File"""

    frameRate: int
    height: int
    wifth: int
    name: str
    size: int
    type: STREAM_TYPES
    StartTime: TimeValue
    EndTime: TimeValue


class SearchResults(TypedDict, total=False):
    """Search Results"""

    channel: int
    Status: list[SearchStatus]
    File: list[SearchFile]
