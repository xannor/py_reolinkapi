"""AI Mixin"""

from ..connection.typing import WithConnection
from ..errors import ReolinkResponseError
from .command import CommandFactory
from .typing import Config


class AI(WithConnection[CommandFactory]):
    """AI Mixin"""

    async def get_ai_state(self, channel: int = 0):
        """Get AI State Info"""

        async for response in self._execute(
            self.commands.create_get_ai_state_request(channel)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Get AI State failed")

            if (
                self.commands.is_get_ai_state_response(response)
                and response.channel_id == channel
            ):
                return response.state

        raise ReolinkResponseError("Get AI State failed")

    async def get_ai_config(self, channel: int = 0):
        """Get AI Config Info"""

        async for response in self._execute(
            self.commands.create_get_ai_config_request(channel)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Get AI State failed")

            if (
                self.commands.is_get_ai_config_response(response)
                and response.channel_id == channel
            ):
                return response.config

        raise ReolinkResponseError("Get AI State failed")

    async def set_ai_config(
        self,
        config: Config,
        channel: int = 0,
    ):
        """Set AI Configuration"""

        async for response in self._execute(
            self.commands.create_set_ai_config(channel, config)
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Set AI State failed")

            if self.commands.is_success(response):
                return True

        raise ReolinkResponseError("Set AI State failed")
