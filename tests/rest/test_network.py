""" test auth mixin """

import logging
import os
from reolinkapi.rest.network import (
    ChannelStatusRequest,
    ChannelStatusResponse,
    Network,
    LocalLinkRequest,
    LocalLinkResponse,
    GetNetworkPortRequest,
    GetNetworkPortResponse,
)

from reolinkapi.rest import Client
from .common import MockConnection

_JSON = {
    LocalLinkRequest: '[{"cmd": "GetLocalLink", "action": 0}]',
    LocalLinkResponse: '[{"cmd": "GetLocalLink", "code": 0, "value":null}]',
    ChannelStatusRequest: '[{"cmd": "GetChannelstatus", "action": 0}]',
    ChannelStatusResponse: '[{"cmd": "GetChannelstatus", "code": 0, "value":null}]',
    GetNetworkPortRequest: '[{"cmd": "GetNetPort", "action": 0}]',
    GetNetworkPortResponse: '[{"cmd": "GetNetPort", "code": 0, "value":null}]',
}


class NetworkTestRig(MockConnection, Network):
    """System test rig"""

    JSON = _JSON


async def test_locallink():
    """local link expected values test"""

    client = NetworkTestRig()
    assert await client.get_local_link()


async def test_live_localink(caplog):
    """local link live test"""

    caplog.set_level(logging.DEBUG)
    client = Client()
    await client.connect(os.environ.get("DEV_IP", "localhost"))
    assert await client.login(
        os.environ.get("DEV_USER", "admin"), os.environ.get("DEV_PASS", "")
    )
    info = await client.get_local_link()
    await info
    await client.disconnect()


async def test_channelstatus():
    """channel status expected values test"""

    client = NetworkTestRig()
    info = await client.get_channel_status()
    assert info is not None


async def test_live_channelstatus(caplog):
    """channel status live test"""

    caplog.set_level(logging.DEBUG)
    client = Client()
    await client.connect(os.environ.get("DEV_IP", "localhost"))
    assert await client.login(
        os.environ.get("DEV_USER", "admin"), os.environ.get("DEV_PASS", "")
    )
    info = await client.get_channel_status()
    assert info
    await client.disconnect()


async def test_ports():
    """get ports expected values test"""

    client = NetworkTestRig()
    info = await client.get_ports()
    assert info is not None


async def test_live_ports(caplog):
    """get ports live test"""

    caplog.set_level(logging.DEBUG)
    client = Client()
    await client.connect(os.environ.get("DEV_IP", "localhost"))
    assert await client.login(
        os.environ.get("DEV_USER", "admin"), os.environ.get("DEV_PASS", "")
    )
    info = await client.get_ports()
    assert info
    await client.disconnect()
