"""Command Typings"""
from __future__ import annotations

from enum import IntEnum
from typing import TypedDict


class CommandRequestTypes(IntEnum):
    """Command Action Types"""

    VALUE_ONLY = 0
    DETAILED = 1


COMMAND_REQUEST_TYPE = "action"


class CommandChannelParameter(TypedDict):
    """Command Request Channel Parameter"""

    channel: int


class CommandRequest(TypedDict):
    """Command Request"""

    cmd: str
    action: int
    param: dict[str, any] | None


class CommandResponse(TypedDict):
    """Comand Response"""

    cmd: str
    code: int
    value: dict


class ErrorCode(TypedDict):
    """Error Code"""

    rspCode: int
    detail: str


class CommandResponseErrorValue(TypedDict):
    """Command Response Error Value"""

    error: ErrorCode
