"""Record"""

from abc import ABC, abstractmethod
from . import connection

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

SNAPSHOT_COMMAND: Final = "Snap"


def create_get_snapshot(channel: int = 0):
    """Create Get Snapshot Request"""

    return (
        CommandRequestWithParam(
            cmd=SNAPSHOT_COMMAND,
            action=CommandRequestTypes.VALUE_ONLY,
            param=CommandChannelParameter(channel=channel),
        ),
    )


class SearchCommandParameter(TypedDict):
    """Search Command Parameters"""

    Search: Search


class SearchCommandResponseValue(TypedDict):
    """Search Command Results"""

    SearchResult: SearchResults


SEARCH_COMMAND: Final = "Search"


def create_search(
    search: Search, _type: CommandRequestTypes = CommandRequestTypes.VALUE_ONLY
):
    """Create Search Request"""
    return CommandRequestWithParam(
        cmd=SEARCH_COMMAND, action=_type, param=SearchCommandParameter(Search=search)
    )


_isSearchCmd = commandHelpers.create_is_command(SEARCH_COMMAND)

_isSearch = commandHelpers.create_value_has_key(
    "SearchResult", SearchCommandResponseValue
)


def get_search_responses(responses: Iterable[CommandResponse]):
    """Get Search Result Responses"""

    return map(
        lambda response: response[COMMAND_RESPONSE_VALUE]["SearchResult"],
        filter(
            _isSearch,
            filter(
                commandHelpers.isvalue,
                filter(_isSearchCmd, responses),
            ),
        ),
    )


def get_search_result_status_dates(results: SearchResults):
    """Get the actual dates from the SearchResults Status"""

    statuses = results.get("Status", [])

    table_tuple = (
        (
            status["year"],
            status["mon"],
            (i for i, c in enumerate(status["table"], 1) if c == "1"),
        )
        for status in statuses
    )
    table_dates = map(
        lambda year_month_days: (
            date(year_month_days[0], year_month_days[1], day)
            for day in year_month_days[2]
        ),
        table_tuple,
    )
    return (date for dates in table_dates for date in dates)
