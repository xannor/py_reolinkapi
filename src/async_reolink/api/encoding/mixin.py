"""Encoding"""

from abc import ABC, abstractmethod
from typing import TypeGuard
from ..connection.model import ErrorResponse, Response
from ..connection.part import Connection as ConnectionPart
from ..errors import ReolinkResponseError

from . import command


class Encoding(ConnectionPart, ABC):
    """Encoding Mixin"""

    @abstractmethod
    def _create_get_encoding(self, channel_id: int) -> command.GetEncodingRequest:
        ...

    @abstractmethod
    def _is_get_encoding_response(
        self, response: Response
    ) -> TypeGuard[command.GetEncodingResponse]:
        ...

    async def get_encoding(self, channel: int = 0):
        """Get Encoding Info"""

        async for response in self._execute(self._create_get_encoding(channel)):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Get Encoding failed")

            if self._is_get_encoding_response(response) and response.channel_id == channel:
                return response.info

        raise ReolinkResponseError("Get Encoding failed")
