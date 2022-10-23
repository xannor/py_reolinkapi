"""Record Commands"""

from datetime import datetime
from typing import Protocol, Sequence, TypeGuard

from ..connection.typing import ChannelValue
from ..connection.typing import CommandFactory as WithCommandFactory
from ..connection.typing import CommandRequest, CommandResponse
from ..typing import StreamTypes
from .typing import File, Search, SearchStatus


class GetSnapshotRequest(CommandRequest, ChannelValue, Protocol):
    """Get Snapshot Request"""


class SearchRecordingsRequest(CommandRequest, ChannelValue, Protocol):
    """Search Recordings Request"""

    search: Search


class SearchRecordingsResponse(CommandResponse, ChannelValue, Protocol):
    """Search Recordings Response"""

    status: Sequence[SearchStatus] | None
    files: Sequence[File] | None


class CommandFactory(WithCommandFactory, Protocol):
    """Record Command Factory"""

    def create_get_snapshot_request(self, channel_id: int) -> GetSnapshotRequest:
        """create GetSnapshotRequest"""

    def create_search_request(
        self,
        channel_id: int,
        start_time: datetime,
        end_time: datetime,
        only_status: bool,
        stream_type: StreamTypes,
    ) -> SearchRecordingsRequest:
        """create SearchRecordingsRequest"""

    def is_search_response(
        self, response: CommandResponse
    ) -> TypeGuard[SearchRecordingsResponse]:
        """is SearchRecordingsResponse"""
