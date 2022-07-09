"""Various Typings and TypeChecks"""

from __future__ import annotations
from enum import IntEnum
from typing import TYPE_CHECKING, NewType

if TYPE_CHECKING:  # typechecker is having issues with the backport
    from enum import Enum

    class StrEnum(str, Enum):
        """String Enum"""

        # pylint: disable=no-self-argument
        def _generate_next_value_(name, *_):
            return name.lower()

else:
    try:
        from enum import StrEnum
    except ImportError:
        from backports.strenum import StrEnum


class OnOffState(IntEnum):
    """On/Off State"""

    OFF = 0
    ON = 1


class BoolState(IntEnum):
    """Boolean State"""

    FALSE = 0
    TRUE = 1


class SetState(IntEnum):
    """Set/Clear State"""

    CLEAR = 0
    SET = 1


IntPercent = NewType("IntPercent", int)
""" An integer within 0 and 100"""

ClockHour = NewType("ClockHour", int)
""" An integer representing a 24 hour cycle """

ClockMinutes = NewType("ClockMinutes", int)
""" An integer repeseting a 60 minute cycle """

ClockSeconds = NewType("ClockSeconds", int)
""" An integer representing a 60 second cycle """
