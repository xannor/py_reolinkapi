""" test auth mixin """

import logging
import os
from reolinkapi.rest.network import (
    Network,
    GET_CHANNEL_STATUS_COMMAND,
    GET_LOCAL_LINK_COMMAND,
    GET_NETWORK_PORT_COMMAND,
    GET_RTSP_URL_COMMAND,
)

from reolinkapi.rest import Client
from .common import MockConnection

_JSON = {
    GET_LOCAL_LINK_COMMAND: (
        '[{"cmd": "GetLocalLink", "action": 0}]',
        '[{"cmd": "GetLocalLink", "code": 0, "value":null}]',
    ),
    GET_CHANNEL_STATUS_COMMAND: (
        '[{"cmd": "GetChannelstatus", "action": 0}]',
        '[{"cmd": "GetChannelstatus", "code": 0, "value":null}]',
    ),
    GET_NETWORK_PORT_COMMAND: (
        '[{"cmd": "GetNetPort", "action": 0}]',
        '[{"cmd": "GetNetPort", "code": 0, "value":null}]',
    ),
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
