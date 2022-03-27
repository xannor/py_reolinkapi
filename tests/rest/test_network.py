""" test auth mixin """

import logging
import os
from reolinkapi.base.network import Network
from reolinkapi.helpers.network import (
    GET_CHANNEL_STATUS_COMMAND,
    GET_LOCAL_LINK_COMMAND,
    GET_NETWORK_PORT_COMMAND,
    GET_P2P_COMMAND,
)

from reolinkapi.rest import Client
from .common import MockConnection

_JSON = {
    GET_LOCAL_LINK_COMMAND: (
        '[{"cmd": "GetLocalLink", "action": 0}]',
        '[{"cmd": "GetLocalLink", "code": 0, "value":{}}]',
    ),
    GET_CHANNEL_STATUS_COMMAND: (
        '[{"cmd": "GetChannelstatus", "action": 0}]',
        '[{"cmd": "GetChannelstatus", "code": 0, "value":{"status":[], "count": 0}}]',
    ),
    GET_NETWORK_PORT_COMMAND: (
        '[{"cmd": "GetNetPort", "action": 0}]',
        '[{"cmd": "GetNetPort", "code": 0, "value":{}}]',
    ),
    GET_P2P_COMMAND: (
        '[{"cmd": "GetP2p", "action": 0}]',
        '[{"cmd": "GetP2p", "code": 0, "value":{"P2p":{}}}]',
    ),
}


class NetworkTestRig(MockConnection, Network):
    """System test rig"""

    JSON = _JSON


async def test_locallink():
    """local link expected values test"""

    client = NetworkTestRig()
    assert await client.get_local_link() is not None


async def test_live_localink(caplog):
    """local link live test"""

    caplog.set_level(logging.DEBUG)
    client = Client()
    await client.connect(os.environ.get("DEV_IP", "localhost"))
    assert await client.login(
        os.environ.get("DEV_USER", "admin"), os.environ.get("DEV_PASS", "")
    )
    info = await client.get_local_link()
    assert info is not None
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
    assert info is not None
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
    assert info is not None
    await client.disconnect()


async def test_p2p():
    """local p2p values test"""

    client = NetworkTestRig()
    assert await client.get_p2p() is not None


async def test_live_p2p(caplog):
    """local p2p test"""

    caplog.set_level(logging.DEBUG)
    client = Client()
    await client.connect(os.environ.get("DEV_IP", "localhost"))
    assert await client.login(
        os.environ.get("DEV_USER", "admin"), os.environ.get("DEV_PASS", "")
    )
    info = await client.get_p2p()
    assert info is not None
    await client.disconnect()
