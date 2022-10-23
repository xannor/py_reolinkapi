"""Network 3.3"""

from ..connection.typing import WithConnection
from ..errors import ReolinkResponseError
from ..system.typing import WithSystem
from ..system.capabilities import ScheduleVersion
from ..typing import StreamTypes
from .command import CommandFactory


class Network(WithConnection[CommandFactory], WithSystem):
    """Network commands Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__link = None
        self.__ports = None
        self.__no_get_rtsp = None

        self._disconnect_callbacks.append(self.__clear)

    def __clear(self):
        self.__no_get_rtsp = False
        self.__link = None
        self.__ports = None

    async def get_local_link(self):
        """Get Local Link"""

        self.__link = None
        async for response in self._execute(
            self.commands.create_get_local_link_request()
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Get local link failed")

            if self.commands.is_get_local_link_response(response):
                link = response.local_link
                self.__link = link
                return link

        raise ReolinkResponseError("Get local link failed")

    async def get_channel_status(self):
        """Get Channel Statuses"""

        async for response in self._execute(
            self.commands.create_get_channel_status_request()
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Get channel status failed")

            if self.commands.is_get_channel_status_response(response):
                return response.channels

        raise ReolinkResponseError("Get channel status failed")

    async def get_ports(self):
        """Get Network Ports"""

        self.__ports = None
        async for response in self._execute(self.commands.create_get_ports_request()):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Get network ports failed")

            if self.commands.is_get_ports_response(response):
                ports = response.ports
                self.__ports = ports
                return ports

        raise ReolinkResponseError("Get network ports failed")

    async def _ensure_ports_and_link(self):

        commands = []

        # pylint: disable=no-member

        if self.__link is None:
            abilities = await self._ensure_capabilities()
            if abilities.local_link:
                commands.append(self.commands.create_get_local_link_request())
        if self.__ports is None:
            commands.append(self.commands.create_get_ports_request())

        if not commands:
            return

        async for response in self._execute(*commands):
            if not self.commands.is_response(response) or self.commands.is_error(
                response
            ):
                break

            if self.commands.is_get_local_link_response(response):
                self.__link = response.local_link
            elif self.commands.is_get_ports_response(response):
                self.__ports = response.ports

    async def get_rtsp_url(
        self, channel: int = 0, stream: StreamTypes = StreamTypes.MAIN
    ):
        """Get RTSP Url"""

        if self.__no_get_rtsp is None:
            self.__no_get_rtsp = True
            abilities = await self._ensure_capabilities()
            self.__no_get_rtsp = (
                abilities.schedule_version.value == ScheduleVersion.BASIC
            )

        if not self.__no_get_rtsp:
            async for response in self._execute(
                self.commands.create_get_rtsp_urls_request(0)
            ):
                if not self.commands.is_response(response) or self.commands.is_error(
                    response
                ):
                    break

                if self.commands.is_get_rtsp_urls_response(response):
                    return response.urls[stream]

            self.__no_get_rtsp = True

        await self._ensure_ports_and_link()

        port = (
            f":{self.__ports.rtsp.value}"
            if self.__ports.rtsp.value not in (0, 554)
            else ""
        )

        url = f"rtsp://{self.__link.ip.address}{port}/h264Preview_{(channel+1):02}_{stream.name.lower()}"
        return url

    async def get_rtmp_url(
        self, channel: int = 0, stream: StreamTypes = StreamTypes.MAIN
    ):
        """Get RTMP Url"""

        await self._ensure_ports_and_link()

        port = (
            f":{self.__ports.rtmp.value}"
            if self.__ports.rtmp.value not in (0, 1935)
            else ""
        )

        url = f"rtmp://{self.__link.ip.address}{port}/bcs/channel{channel}_{stream.name.lower()}.bcs?channel={channel}&stream={stream.name.lower()}"
        return url

    async def get_p2p(self):
        """Get P2P"""

        async for response in self._execute(self.commands.create_get_p2p_request()):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Get p2p info failed")

            if self.commands.is_get_p2p_response(response):
                return response.info

        raise ReolinkResponseError("Get p2p info failed")

    async def get_wifi(self):
        """Get Wifi Info"""

        async for response in self._execute(
            self.commands.create_get_wifi_info_request()
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Get wifi info failed")

            if self.commands.is_get_wifi_info_response(response):
                return response.info

        raise ReolinkResponseError("Get wifi info failed")

    async def get_wifi_signal(self):
        """Get Wifi Signal Strength"""

        async for response in self._execute(
            self.commands.create_get_wifi_signal_request()
        ):
            if not self.commands.is_response(response):
                break

            if self.commands.is_error(response):
                response.throw("Get wifi signal failed")

            if self.commands.is_get_wifi_signal_response(response):
                return response.signal

        raise ReolinkResponseError("Get wifi signal failed")
