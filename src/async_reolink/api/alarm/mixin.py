"""Alarm"""

from abc import ABC, abstractmethod
from typing import TypeGuard
from ..connection.model import ErrorResponse, Response
from ..connection.part import Connection as ConnectionPart
from ..errors import ReolinkResponseError

from . import command


class Alarm(ConnectionPart, ABC):
    """Alarm Mixin"""

    @abstractmethod
    def _create_get_md_state(self, channel_id: int) -> command.GetMotionStateRequest:
        ...

    @abstractmethod
    def _is_get_md_response(self, response: Response) -> TypeGuard[command.GetMotionStateResponse]:
        ...

    async def get_md_state(self, channel: int = 0):
        """Get Motion Detection Info"""

        async for response in self._execute(self._create_get_md_state(channel)):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Get Motion State failed")

            if self._is_get_md_response(response):
                return response.state

        raise ReolinkResponseError("Get Motion State failed")
