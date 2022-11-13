"""Record Commands"""

from typing import Protocol, Sequence

from ..connection.typing import ChannelValue
from .typing import File, Search, SearchStatus


class GetSnapshotRequest(ChannelValue, Protocol):
    """Get Snapshot Request"""


class SearchRecordingsRequest(ChannelValue, Protocol):
    """Search Recordings Request"""

    search: Search


class SearchRecordingsResponse(ChannelValue, Protocol):
    """Search Recordings Response"""

    status: Sequence[SearchStatus] | None
    files: Sequence[File] | None
