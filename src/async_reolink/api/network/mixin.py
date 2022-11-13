"""Network 3.3"""

from abc import ABC, abstractmethod
from typing import TypeGuard

from ..connection.model import ErrorResponse, Response
from ..connection.part import Connection as ConnectionPart
from ..errors import ReolinkResponseError
from ..system.part import System as SystemPart
from ..system.capabilities import ScheduleVersion
from ..typing import StreamTypes

from . import command


class Network(ConnectionPart, SystemPart, ABC):
    """Network commands Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__no_get_rtsp = None

        self._disconnect_callbacks.append(self.__clear)

    def __clear(self):
        self.__no_get_rtsp = False

    @abstractmethod
    def _create_get_local_link(self) -> command.GetLocalLinkRequest:
        ...

    @abstractmethod
    def _is_get_local_link_response(
        self, response: Response
    ) -> TypeGuard[command.GetLocalLinkResponse]:
        ...

    async def get_local_link(self):
        """Get Local Link"""

        async for response in self._execute(self._create_get_local_link()):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Get local link failed")

            if self._is_get_local_link_response(response):
                return response.local_link

        raise ReolinkResponseError("Get local link failed")

    @abstractmethod
    def _create_get_channel_status(self) -> command.GetChannelStatusRequest:
        ...

    @abstractmethod
    def _is_get_channel_status_response(
        self, response: Response
    ) -> TypeGuard[command.GetChannelStatusResponse]:
        ...

    async def get_channel_status(self):
        """Get Channel Statuses"""

        async for response in self._execute(self._create_get_channel_status()):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Get channel status failed")

            if self._is_get_channel_status_response(response):
                return response.channels

        raise ReolinkResponseError("Get channel status failed")

    @abstractmethod
    def _create_get_ports(self) -> command.GetNetworkPortsRequest:
        ...

    @abstractmethod
    def _is_get_ports_response(
        self, response: Response
    ) -> TypeGuard[command.GetNetworkPortsResponse]:
        ...

    async def get_ports(self):
        """Get Network Ports"""

        async for response in self._execute(self._create_get_ports()):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Get network ports failed")

            if self._is_get_ports_response(response):
                return response.ports

        raise ReolinkResponseError("Get network ports failed")

    @abstractmethod
    def _create_get_rtsp_urls(self, channel_id: int) -> command.GetRTSPUrlsRequest:
        ...

    @abstractmethod
    def _is_get_rtsp_urls_response(
        self, response: Response
    ) -> TypeGuard[command.GetRTSPUrlsResponse]:
        ...

    async def get_rtsp_url(self, channel: int = 0, stream: StreamTypes = StreamTypes.MAIN):
        """Get RTSP Url"""

        if self.__no_get_rtsp is None:
            self.__no_get_rtsp = True
            abilities = await self.get_capabilities()
            self.__no_get_rtsp = abilities.schedule_version.value == ScheduleVersion.BASIC

        if not self.__no_get_rtsp:
            async for response in self._execute(self._create_get_rtsp_urls(0)):
                if not self._is_response(response) or self._is_error(response):
                    break

                if self._is_get_rtsp_urls_response(response):
                    return response.urls[stream]

            self.__no_get_rtsp = True

        ports = await self.get_ports()

        port = f":{ports.rtsp.value}" if ports.rtsp.value not in (0, 554) else ""

        url = f"rtsp://{self.hostname}{port}/h264Preview_{(channel+1):02}_{stream.name.lower()}"
        return url

    async def get_rtmp_url(self, channel: int = 0, stream: StreamTypes = StreamTypes.MAIN):
        """Get RTMP Url"""

        ports = await self.get_ports()

        port = f":{ports.rtmp.value}" if ports.rtmp.value not in (0, 1935) else ""

        url = f"rtmp://{self.hostname}{port}/bcs/channel{channel}_{stream.name.lower()}.bcs?channel={channel}&stream={stream.name.lower()}"
        return url

    @abstractmethod
    def _create_get_p2p(self) -> command.GetP2PRequest:
        ...

    @abstractmethod
    def _is_get_p2p_response(self, response: Response) -> TypeGuard[command.GetP2PResponse]:
        ...

    async def get_p2p(self):
        """Get P2P"""

        async for response in self._execute(self._create_get_p2p()):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Get p2p info failed")

            if self._is_get_p2p_response(response):
                return response.info

        raise ReolinkResponseError("Get p2p info failed")

    @abstractmethod
    def _create_get_wifi_info(self) -> command.GetWifiInfoRequest:
        ...

    @abstractmethod
    def _is_get_wifi_info_response(
        self, response: Response
    ) -> TypeGuard[command.GetWifiInfoResponse]:
        ...

    async def get_wifi(self):
        """Get Wifi Info"""

        async for response in self._execute(self._create_get_wifi_info()):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Get wifi info failed")

            if self._is_get_wifi_info_response(response):
                return response.info

        raise ReolinkResponseError("Get wifi info failed")

    @abstractmethod
    def _create_get_wifi_signal(self) -> command.GetWifiSignalRequest:
        ...

    @abstractmethod
    def _is_get_wifi_signal_response(
        self, response: Response
    ) -> TypeGuard[command.GetWifiSignalResponse]:
        ...

    async def get_wifi_signal(self):
        """Get Wifi Signal Strength"""

        async for response in self._execute(self._create_get_wifi_signal()):
            if not isinstance(response, Response):
                break

            if isinstance(response, ErrorResponse):
                response.throw("Get wifi signal failed")

            if self._is_get_wifi_signal_response(response):
                return response.signal

        raise ReolinkResponseError("Get wifi signal failed")
