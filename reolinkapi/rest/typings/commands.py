"""Command Typings"""
from __future__ import annotations

from enum import IntEnum
from typing import Iterable, TypedDict


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


def filter_command_responses(cmd: str, responses: Iterable[CommandResponse]):
    """filter responses for command successes"""
    return filter(
        lambda response: response["cmd"] == cmd and "value" in response, responses
    )


def filter_command_errors(cmd: str, responses: Iterable[CommandResponse]):
    """filter responses for command errors"""

    def _cast(response: CommandResponse):
        error: CommandResponseErrorValue = response["error"]
        return error["error"]

    return map(
        _cast,
        filter(
            lambda response: response["cmd"] == cmd and "error" in response, responses
        ),
    )


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
