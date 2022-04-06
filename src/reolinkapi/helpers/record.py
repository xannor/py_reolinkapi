"""Record Helpers"""

from datetime import date
from typing import Final, Iterable, TypedDict

from ..typings.commands import (
    COMMAND_RESPONSE_VALUE,
    CommandChannelParameter,
    CommandRequestTypes,
    CommandRequestWithParam,
    CommandResponse,
)

from ..helpers import commands as commandHelpers
from ..typings.record import Search, SearchResults

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
