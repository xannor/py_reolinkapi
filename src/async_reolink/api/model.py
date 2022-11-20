"""Models"""

from abc import ABC
from datetime import date, datetime, time
from . import typing


class Date(typing.Date, ABC):
    """Date"""

    # pylint: disable=no-self-argument
    def to_date(__date: typing.Date):
        """convert Date to date"""
        return date(__date.year, __date.month, __date.day)


class SimpleTime(typing.SimpleTime, ABC):
    """Simple Time"""

    # pylint: disable=no-self-argument
    def to_time(__time: typing.SimpleTime):
        """convert SimpleTime to time"""
        return time(__time.hour, __time.minute, 0)


class Time(typing.Time, ABC):
    """Time"""

    # pylint: disable=no-self-argument
    def to_time(__time: typing.Time):
        """convert Time to time"""
        return time(__time.hour, __time.minute, __time.second)


class DateTime(typing.DateTime, Date, Time, ABC):
    """Date and Time"""

    # pylint: disable=no-self-argument
    def to_datetime(__datetime: typing.DateTime):
        """convert DateTime to datetime"""
        if isinstance(__datetime, DateTime):
            return datetime.combine(__datetime.to_date(), __datetime.to_time())
        return datetime.combine(Date.to_date(__datetime), Time.to_time(__datetime))
