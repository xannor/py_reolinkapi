"""Network Mixin"""
from __future__ import annotations

from . import connection, security

from ..typings.network import LinkInfo, NetworkPorts

from ..const import StreamTypes
from ..helpers import network as networkHelpers


class Network:
    """Network commands Mixin"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__link: LinkInfo | None = None
        self.__ports: NetworkPorts | None = None
        self.__no_get_rtsp = False
        if isinstance(self, connection.Connection):
            self._disconnect_callbacks.append(self.__clear)

    def __clear(self):
        self.__no_get_rtsp = False
        self.__link = None
        self.__ports = None

    async def get_local_link(self):
        """Get Local Link"""

        self.__link = None
        self.__ports = None
        if isinstance(self, connection.Connection):
            responses = await self._execute(networkHelpers.create_get_local_link())
        else:
            return None

        link = next(networkHelpers.get_local_link_responses(responses), None)
        if link is not None:
            self.__link = link
        return link

    async def get_channel_status(self):
        """Get Channel Statuses Link"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(networkHelpers.create_get_channel_status())
        else:
            return None

        status = next(networkHelpers.get_channel_status_responses(responses), None)
        if status is not None:
            return status["status"]

    async def get_ports(self):
        """Get Network Ports Url"""

        self.__ports = None
        if isinstance(self, connection.Connection):
            responses = await self._execute(networkHelpers.create_get_network_ports())
        else:
            return None

        ports = next(networkHelpers.get_network_ports_responses(responses), None)
        if ports is not None:
            self.__ports = ports
        return ports

    async def _ensure_ports_and_link(self):
        commands = []
        if self.__link is None:
            commands.append(networkHelpers.create_get_local_link())
        if self.__ports is None:
            commands.append(networkHelpers.create_get_network_ports())

        if len(commands) > 0 and isinstance(self, connection.Connection):
            responses = await self._execute(*commands)
        else:
            responses = []

        link = next(networkHelpers.get_local_link_responses(responses), None)
        ports = next(networkHelpers.get_network_ports_responses(responses), None)
        if link is not None:
            self.__link = link
        if ports is not None:
            self.__ports = ports

    async def get_rtsp_url(
        self, channel: int = 0, stream: StreamTypes = StreamTypes.MAIN
    ):
        """Get RTSP Url"""

        if not self.__no_get_rtsp:
            responses = None
            if isinstance(self, connection.Connection):
                responses = await self._execute(networkHelpers.create_get_rtsp_url())

            if responses is not None:
                urls = next(networkHelpers.get_rtsp_url_responses(responses), None)
                if not urls is None:
                    url: str = urls[f"{stream.name.lower()}Stream"]
                    # if isinstance(self, security.Security) and self._auth_token != "":
                    #    return f"{url}&token={self._auth_token}"
                    return url

            self.__no_get_rtsp = True

        await self._ensure_ports_and_link()

        port = (
            f':{self.__ports["rtspPort"]}'
            if self.__ports["rtspPort"] not in (0, 554)
            else ""
        )

        url = f'rtsp://{self.__link["static"]["ip"]}{port}/h264Preview_{(channel+1):02}_{stream.name.lower()}'
        # if isinstance(self, security.Security) and self._auth_token != "":
        #    return f"{url}&token={self._auth_token}"
        return url

    async def get_rtmp_url(
        self, channel: int = 0, stream: StreamTypes = StreamTypes.MAIN
    ):
        """Get RTMP Url"""

        await self._ensure_ports_and_link()

        port = (
            f':{self.__ports["rtmpPort"]}'
            if self.__ports["rtmpPort"] not in (0, 1935)
            else ""
        )

        url = f'rtmp://{self.__link["static"]["ip"]}{port}/bcs/channel{channel}_{stream.name.lower()}.bcs?channel={channel}&stream={stream}'
        if isinstance(self, security.Security):
            if self._auth_token != "":
                return f"{url}&token={self._auth_token}"
        return url

    async def get_p2p(self):
        """Get P2P"""

        if isinstance(self, connection.Connection):
            responses = await self._execute(networkHelpers.create_get_p2p())
        else:
            return None

        return next(networkHelpers.get_p2p_responses(responses), None)
