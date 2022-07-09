"""Record"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from time import time
from typing import Final, Iterable, MutableMapping, TypedDict
from typing_extensions import TypeGuard

from .errors import ReolinkStreamResponseError

from .utils import anext, afilter, amap, alist


from .commands import (
    CommandChannelParameter,
    CommandRequestTypes,
    CommandRequestWithParam,
    CommandResponseType,
    CommandResponseValue,
    async_trap_errors,
)
from . import connection
from . import system

from .const import StreamTypes


@dataclass
class Search:
    """Search"""

    channel: int
    onlyStatus: int  # pylint: disable=invalid-name
    streamType: StreamTypes  # pylint: disable=invalid-name
    StartTime: system.TimeValue  # pylint: disable=invalid-name
    EndTime: system.TimeValue  # pylint: disable=invalid-name


class SearchStatusTable(MutableMapping[int, bool]):
    """Search Status Table"""

    def __init__(self, table: str = None) -> None:
        self._table: dict[int, bool] = dict()
        if table is not None:
            for (i, _c) in enumerate(table, 1):
                self._table[i] = _c == "1"

    def __getitem__(self, __k: int):
        return self._table.__getitem__(__k)

    def __setitem__(self, __k: int, __v: bool) -> None:
        return self._table.__setitem__(__k, __v)

    def __delitem__(self, __v: int):
        return self._table.__delitem__(__v)

    def __iter__(self):
        return self._table.__iter__()

    def __len__(self):
        return self._table.__len__()

    def __str__(self) -> str:
        return "".join(("1" if b else "0") for (_, b) in self._table.items())


@dataclass
class SearchStatus(Iterable[date]):
    """Search Result Status"""

    month: int
    year: int
    table: SearchStatusTable

    @classmethod
    def from_dict(cls, value: SearchStatusType):
        """Convert results json to class"""
        return cls(value["mon"], value["year"], SearchStatusTable(value["table"]))

    def __iter__(self):
        for (i, _b) in self.table.items():
            if _b:
                yield date(self.year, self.month, i)


class SearchStatusType(TypedDict):
    """Search Result Status"""

    mon: int
    year: int
    table: str


class SearchFileType(TypedDict):
    """Search Result File"""

    frameRate: int
    height: int
    wifth: int
    name: str
    size: int
    type: str
    StartTime: system.TimeValueType
    EndTime: system.TimeValueType


class SearchResultsType(TypedDict, total=False):
    """Search Results"""

    channel: int
    Status: list[SearchStatusType]
    File: list[SearchFileType]


class Record:
    """Record Mixin"""

    async def get_snap(self, channel: int = 0):
        """get snapshot"""

        if not isinstance(self, connection.Connection):
            return None

        responses = self._execute(  # pylint: disable=no-member
            SnapshotCommand(channel),
        )

        if responses is None:
            return None

        buffer = bytearray()

        async for response in responses:
            if not isinstance(response, (bytes, bytearray)):
                await alist(async_trap_errors(response))
                raise ReolinkStreamResponseError()
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
        camera_time = None
        if isinstance(self, system.System):
            camera_time = await self._ensure_time()
        tzinfo = camera_time.tzinfo if camera_time is not None else None

        if end_time is None:
            end_time = datetime.combine(
                datetime.now(tzinfo).date(), time.min, tzinfo)
            end_time += timedelta(days=1, seconds=-1)
        elif end_time.tzinfo is not None:
            end_time = end_time.astimezone(tzinfo)

        if start_time is None:
            start_time = datetime.combine(
                end_time.date(), time.min, end_time.tzinfo)
        elif start_time.tzinfo is not None:
            start_time = start_time.astimezone(tzinfo)

        search = Search(
            channel=channel,
            onlyStatus=1 if only_status else 0,
            streamType=stream_type,
            StartTime=system.TimeValue.from_datetime(start_time),
            EndTime=system.TimeValue.from_datetime(end_time),
        )
        if only_status:
            search["onlyStatus"] = 1

        if not isinstance(self, connection.Connection):
            return None

        responses = async_trap_errors(self._execute(  # pylint: disable=no-member
            SearchCommand(search)
        ))

        return await anext(
            amap(
                SearchCommand.get_value,
                afilter(SearchCommand.is_response, responses)
            ),
            None
        )

    async def search_status(
        self,
        channel: int = 0,
        *,
        start_time: datetime = None,
        end_time: datetime = None,
        stream_type: StreamTypes = StreamTypes.MAIN
    ):
        """Perform search but only return available dates in month range"""
        results = await self._search(start_time, end_time, channel, True, stream_type)
        if results is None:
            return SearchStatus(0, 0, SearchStatusTable())
        return SearchStatus.from_dict(results["Status"])

    async def search(
        self,
        channel: int = 0,
        *,
        start_time: datetime = None,
        end_time: datetime = None,
        stream_type: StreamTypes = StreamTypes.MAIN
    ):
        """Search for recordings in range"""
        results = await self._search(start_time, end_time, channel, False, stream_type)
        if results is None:
            return []
        return list(
            file
            for file in results.get("File", [])
        )


class SnapshotCommand(CommandRequestWithParam[CommandChannelParameter]):
    """Get Snapshot"""

    COMMAND: Final = "Snap"

    def __init__(
        self,
        channel: int = 0,
        requestType: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY
    ):
        super().__init__(type(self).COMMAND, requestType, CommandChannelParameter(channel))


@dataclass
class SearchCommandParameter:
    """Search Command Parameters"""

    Search: Search  # pylint: disable=invalid-name


class SearchCommandResponseValueType(TypedDict):
    """Search Command Results"""

    SearchResult: SearchResultsType


class SearchCommandResponseType(CommandResponseType, total=False):
    """Search Command Response"""

    value: SearchCommandResponseValueType


class SearchCommand(CommandRequestWithParam[SearchCommandParameter]):
    """Search Command"""

    COMMAND: Final = "Search"
    RESPONSE: Final = "SearchResult"

    def __init__(
        self,
        search: Search,
        request_type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY,
    ):
        super().__init__(type(self).COMMAND, request_type, SearchCommandParameter(search))

    @classmethod
    def is_response(cls, value: any) -> TypeGuard[CommandResponseValue[SearchCommandResponseValueType]]:  # pylint: disable=arguments-differ
        """Is response a search result"""
        return (
            super().is_response(value, command=cls.COMMAND)
            and super()._is_typed_value(value, cls.RESPONSE, SearchCommandResponseValueType)
        )

    @classmethod
    def get_value(cls, value: CommandResponseValue[SearchCommandResponseValueType]):
        """Get Channel Status Response"""
        return cls._get_value(value)[  # pylint: disable=unsubscriptable-object
            cls.RESPONSE
        ]
