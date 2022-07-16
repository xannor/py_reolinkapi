"""Various Typings and TypeChecks"""

from __future__ import annotations
from enum import IntEnum
from typing import NewType


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
