"""Command Typings"""
from __future__ import annotations

from enum import IntEnum
from typing import Final, Literal, TypedDict
from typing_extensions import NotRequired


class CommandRequestTypes(IntEnum):
    """Command Action Types"""

    VALUE_ONLY = 0
    DETAILED = 1


COMMAND_REQUEST_TYPE: Final = "action"


class CommandChannelParameter(TypedDict):
    """Command Request Channel Parameter"""

    channel: int


class CommandRequest(TypedDict, total=True):
    """Command Request"""

    cmd: str
    action: int


# this should be generic but they are not supported yet
class CommandRequestWithParam(CommandRequest, total=False):
    """Command Request"""

    param: dict[str, any]


COMMAND_REQUEST_PARAM: Final = "param"
COMMAND_REQUEST_PARAM_LITERAL: Final = Literal["param"]


class CommandResponse(TypedDict):
    """Comand Response"""

    cmd: str
    code: int


COMMAND: Final = "cmd"

# this should be generic but they are not supported yet
class CommandResponseValue(CommandResponse):
    """Comand Response Value"""

    value: dict
    initial: NotRequired[dict]
    range: NotRequired[dict]


COMMAND_RESPONSE_VALUE: Final = "value"
COMMAND_RESPONSE_VALUE_LITERAL: Final = Literal["value"]


class CommandResponseCodeValue(TypedDict):
    """Command Response Code Value"""

    rspCode: int


COMMAND_RESPONSE_CODE: Final = "rspCode"


class ErrorCode(TypedDict):
    """Error Code"""

    rspCode: int
    detail: str


class CommandResponseErrorValue(CommandResponse):
    """Command Response Error Value"""

    error: ErrorCode


COMMAND_RESPONSE_ERROR: Final = "error"
