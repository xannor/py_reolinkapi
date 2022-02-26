""" commands """

from abc import ABC
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Callable, TypeVar, overload

from ..utils.dataclasses import keyword


@dataclass
class Command(ABC):
    """Abstract Command"""

    command: str = field(init=False, metadata=keyword("cmd"))


class RequestTypes(IntEnum):
    """Type of request"""

    VALUEONLY = 0
    DETAILED = 1


@dataclass
class CommandRequestParameter(ABC):
    """Abstract Command Request Parameter"""


@dataclass
class CommandRequest(Command, ABC):
    """Abstract Command Request"""

    type: RequestTypes = field(
        default=RequestTypes.VALUEONLY, init=False, metadata=keyword("action")
    )
    param: CommandRequestParameter = field(init=False)


@dataclass
class CommandResponse(Command, ABC):
    """Abstract Command Response"""


@dataclass
class ErrorCode:
    """Error Code"""

    code: int = field(metadata=keyword("rspCode"))
    detail: str = field()


@dataclass
class CommandError(CommandResponse):
    """Command Error Response"""

    error: ErrorCode = field()


@dataclass
class UnknownCommandResponse(CommandResponse):
    """Unknown Command Response"""

    value: dict = field()


@dataclass
class CommandValueResponseValue(ABC):
    """Abstract Command Response Value"""


@dataclass
class CommandValueResponse(CommandResponse, ABC):
    """Abstract Command Response Value"""

    value: CommandValueResponseValue = field(init=False)


_RESPONSE_TYPE = "__command_response_type__"

_T = TypeVar("_T")


@overload
def response_type(__type: type) -> Callable[[type[_T]], type[_T]]:
    """Define Response type"""


def response_type(__type: type):
    """Define Response type"""

    def wrap(cls):
        setattr(cls, _RESPONSE_TYPE, __type)
        return cls

    return wrap


@overload
def get_response_type(class_or_instance: any) -> type[CommandResponse]:
    """Get defined Response Type"""


def get_response_type(class_or_instance: any):
    """Get defined Response Type"""
    if not isinstance(class_or_instance, type):
        class_or_instance = type(class_or_instance)
    return getattr(class_or_instance, _RESPONSE_TYPE)
