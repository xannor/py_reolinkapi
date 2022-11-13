"""AI Mixin"""

from abc import ABC, abstractmethod
from typing import TypeGuard
from ..connection.part import Connection as ConnectionPart
from ..connection.model import Response, ErrorResponse
from ..errors import ReolinkResponseError
from .typing import Config
from . import command


class AI(ConnectionPart, ABC):
    """AI Mixin"""

    @abstractmethod
    def _create_get_ai_state(self, channel: int) -> command.GetAiStateRequest:
        ...

    @abstractmethod
    def _is_get_ai_state_response(
        self, response: Response
    ) -> TypeGuard[command.GetAiStateResponse]:
        ...

    async def get_ai_state(self, channel: int = 0):
        """Get AI State Info"""

        async for response in self._execute(self._create_get_ai_state(channel)):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Get AI State failed")

            if self._is_get_ai_state_response(response) and response.channel_id == channel:
                return response.state

        raise ReolinkResponseError("Get AI State failed")

    @abstractmethod
    def _create_get_ai_config(self, channel: int) -> command.GetAiConfigRequest:
        ...

    @abstractmethod
    def _is_get_ai_config_response(
        self, response: Response
    ) -> TypeGuard[command.GetAiConfigResponse]:
        ...

    async def get_ai_config(self, channel: int = 0):
        """Get AI Config Info"""

        async for response in self._execute(self._create_get_ai_config(channel)):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Get AI Config failed")

            if self._is_get_ai_config_response(response) and response.channel_id == channel:
                return response.config

        raise ReolinkResponseError("Get AI State failed")

    @abstractmethod
    def _create_set_ai_config(self, channel: int, config: Config) -> command.SetAiConfigRequest:
        ...

    async def set_ai_config(
        self,
        config: Config,
        channel: int = 0,
    ):
        """Set AI Configuration"""

        async for response in self._execute(self._create_set_ai_config(channel, config)):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Set AI Config failed")

            if self._is_success_response(response):
                return True

        raise ReolinkResponseError("Set AI Config failed")
