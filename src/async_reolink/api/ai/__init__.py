"""AI Mixin"""


from abc import ABC, abstractmethod
from typing import Mapping

from ..errors import ErrorCodes, ReolinkResponseError

from ..commands import CommandErrorResponse, ResponseCode
from ..commands.ai import (
    GetAiConfigRequest,
    GetAiConfigResponse,
    GetAiStateRequest,
    GetAiStateResponse,
    SetAiConfigRequest,
)

from .typings import AITypes

from .. import connection


class AI(ABC):
    """AI Mixin"""

    @abstractmethod
    def _create_get_ai_state_request(self, channel: int) -> GetAiStateRequest:
        ...

    async def get_ai_state(self, channel: int = 0):
        """Get AI State Info"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_get_ai_state_request(channel)
            ):
                if (
                    isinstance(response, GetAiStateResponse)
                    and response.channel_id == channel
                ):
                    return response

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get AI State failed")

        raise ReolinkResponseError("Get AI State failed")

    @abstractmethod
    def _create_get_ai_config_request(self, channel: int) -> GetAiConfigRequest:
        ...

    async def get_ai_config(self, channel: int = 0):
        """Get AI Config Info"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_get_ai_config_request(channel)
            ):
                if (
                    isinstance(response, GetAiConfigResponse)
                    and response.channel_id == channel
                ):
                    return response

                if isinstance(response, CommandErrorResponse):
                    response.throw("Get AI State failed")

        raise ReolinkResponseError("Get AI State failed")

    @abstractmethod
    def _create_set_ai_config(
        self,
        channel: int,
        detect: AITypes | set[AITypes] | Mapping[AITypes, bool] | None,
        track: AITypes | set[AITypes] | Mapping[AITypes, bool] | None,
    ) -> SetAiConfigRequest:
        ...

    async def set_ai_config(
        self,
        channel: int = 0,
        detect: AITypes | set[AITypes] | Mapping[AITypes, bool] | None = None,
        track: AITypes | set[AITypes] | Mapping[AITypes, bool] | None = None,
    ):
        """Set AI Configuration"""

        if isinstance(self, connection.Connection):
            async for response in self._execute(
                self._create_set_ai_config(channel, detect, track)
            ):
                if isinstance(response, CommandErrorResponse):
                    response.throw("Set AI State failed")

                if isinstance(response, ResponseCode):
                    return True

        raise ReolinkResponseError("Set AI State failed")
