"""Alarm"""

from ..connection.typing import WithConnection
from ..errors import ReolinkResponseError
from .command import CommandFactory


class Alarm(WithConnection[CommandFactory]):
    """Alarm Mixin"""

    async def get_md_state(self, channel: int = 0):
        """Get Motion Detection Info"""

        async for response in self._execute(self.commands.create_get_md_state(channel)):
            if not self.commands.is_response(response):
                break

            if self.commands.is_get_md_response(response):
                return response.state

            if self.commands.is_error(response):
                response.throw("Get Motion State failed")

        raise ReolinkResponseError("Get Motion State failed")
