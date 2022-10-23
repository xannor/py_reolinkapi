"""Encoding"""

from ..connection.typing import WithConnection
from ..errors import ReolinkResponseError
from .command import CommandFactory


class Encoding(WithConnection[CommandFactory]):
    """Encoding Mixin"""

    async def get_encoding(self, channel: int = 0):
        """Get Encoding Info"""

        async for response in self._execute(
            self.commands.create_get_encoding_request(channel)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Get AI State failed")

            if (
                self.commands.is_get_encoding_response(response)
                and response.channel_id == channel
            ):
                return response.info

        raise ReolinkResponseError("Get AI State failed")
