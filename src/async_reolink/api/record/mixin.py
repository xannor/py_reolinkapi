"""Record"""

from datetime import datetime, time, timedelta
from typing import Sequence

from ..connection.typing import WithConnection
from ..errors import ReolinkResponseError
from ..system.typing import WithSystem
from ..typing import StreamTypes
from .command import CommandFactory
from .typing import File, SearchStatus


class Record(WithConnection[CommandFactory], WithSystem):
    """Record Mixin"""

    async def get_snap(self, channel: int = 0):
        """get snapshot"""

        buffer = bytearray()
        async for response in self._execute(
            self.commands.create_get_snapshot_request(channel)
        ):
            if self.commands.is_response(response) and self.commands.is_error(response):
                response.throw("Get Snap failed")

            if not isinstance(response, bytes):
                raise ReolinkResponseError("Get Snap failed")

            buffer += bytearray(response)

        return bytes(buffer)

    async def _search(
        self,
        start_time: datetime,
        end_time: datetime,
        channel: int,
        only_status: bool,
        stream_type: StreamTypes,
    ):
        camera_time = await self._ensure_time()
        tzinfo = camera_time.tzinfo if camera_time is not None else None

        if end_time is None:
            end_time = datetime.combine(datetime.now(tzinfo).date(), time.min, tzinfo)
            end_time += timedelta(days=1, seconds=-1)
        elif end_time.tzinfo is not None:
            end_time = end_time.astimezone(tzinfo)

        if start_time is None:
            start_time = datetime.combine(end_time.date(), time.min, end_time.tzinfo)
        elif start_time.tzinfo is not None:
            start_time = start_time.astimezone(tzinfo)

        async for response in self._execute(
            self.commands.create_search_request(
                channel, start_time, end_time, only_status, stream_type
            )
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Search failed")

            if self.commands.is_search_response(response):
                return response

        raise ReolinkResponseError("Search failed")

    async def search_status(
        self,
        channel: int = 0,
        *,
        start_time: datetime = None,
        end_time: datetime = None,
        stream_type: StreamTypes = StreamTypes.MAIN,
    ) -> Sequence[SearchStatus]:
        """Perform search but only return available dates in month range"""
        status = (
            await self._search(start_time, end_time, channel, True, stream_type)
        ).status
        if status is None:
            status = []
        return status

    async def search(
        self,
        channel: int = 0,
        *,
        start_time: datetime = None,
        end_time: datetime = None,
        stream_type: StreamTypes = StreamTypes.MAIN,
    ) -> Sequence[File]:
        """Search for recordings in range"""
        files = (
            await self._search(start_time, end_time, channel, False, stream_type)
        ).files
        if files is None:
            files = []
        return files
