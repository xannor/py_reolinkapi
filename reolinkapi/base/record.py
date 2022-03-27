"""Record command"""

from abc import ABC, abstractmethod
from datetime import datetime, time, timedelta

from ..const import STREAM_TYPES

from ..typings.record import Search

from ..helpers import record as recordHelpers, system as systemHelpers

from . import connection, system


class Record(ABC):
    """Record Mixin"""

    @abstractmethod
    async def get_snap(self, channel: int = 0) -> bytes:
        """get snapshot"""
        ...

    async def _search(
        self,
        start_time: datetime,
        end_time: datetime,
        channel: int,
        only_status: bool,
        stream_type: STREAM_TYPES,
    ):
        camera_time = None
        if isinstance(self, system.System):
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

        search = Search(
            channel=channel,
            onlyStatus=1 if only_status else 0,
            streamType=stream_type,
            StartTime=systemHelpers.as_time_value(start_time),
            EndTime=systemHelpers.as_time_value(end_time),
        )
        if only_status:
            search["onlyStatus"] = 1

        if isinstance(self, connection.Connection):
            responses = await self._execute(recordHelpers.create_search(search))
        else:
            return None

        return recordHelpers.get_search_responses(responses)

    async def search_status(
        self,
        channel: int = 0,
        *,
        start_time: datetime = None,
        end_time: datetime = None,
        stream_type: STREAM_TYPES = "main"
    ):
        """Perform search but only return available dates in month range"""
        results = await self._search(start_time, end_time, channel, True, stream_type)
        if results is None:
            return []
        return list(
            date
            for search_results in results
            for date in recordHelpers.get_search_result_status_dates(search_results)
        )

    async def search(
        self,
        channel: int = 0,
        *,
        start_time: datetime = None,
        end_time: datetime = None,
        stream_type: STREAM_TYPES = "main"
    ):
        """Search for recordings in range"""
        results = await self._search(start_time, end_time, channel, False, stream_type)
        if results is None:
            return []
        return list(
            file
            for search_results in results
            for file in search_results.get("File", [])
        )
