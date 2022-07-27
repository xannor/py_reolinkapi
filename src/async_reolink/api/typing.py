"""Various Typings and TypeChecks"""

from __future__ import annotations
from enum import IntEnum
from typing import Annotated, Sequence, TypeGuard, TypeVar, get_args


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


_ST = TypeVar("_ST", bound=Sequence)


def validate_in(sequence: _ST):
    """Create validator for value in given sequence"""
    def validator(value):
        return value in sequence

    return validator


#pylint: disable=redefined-builtin
def validate_length(max: int, min: int = 0):
    """Create validator for a min/max len()"""
    def validator(value):
        return min <= len(value) <= max

    return validator


_A = TypeVar("_A", bound=Annotated)


def isannotated(value: any, __type: type[_A]) -> TypeGuard[_A]:
    """Value is annotated value"""
    (__a_type, *args) = get_args(__type)
    if not isinstance(value, __a_type):
        try:
            value = __a_type(value)
        except Exception:  # pylint: disable=broad-except
            return False
    for test in args:
        if not test(value):
            return False
    return True


IntBool = Annotated[int, validate_in(range(0, 1))]
""" An integer representing a boolean 0 = False, 1 = True """

IntPercent = Annotated[int, validate_in(range(0, 100))]
""" An integer representing a percentage (0..100) """

ClockHour = Annotated[int, validate_in(range(0, 24))]
""" An integer representing a 24 hour cycle """

ClockMinutes = Annotated[int, validate_in(range(0, 59))]
""" An integer repeseting a 60 minute cycle """

ClockSeconds = Annotated[int, validate_in(range(0, 59))]
""" An integer representing a 60 second cycle """
