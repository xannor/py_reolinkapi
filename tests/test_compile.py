"""Will it build?"""

from async_reolink.api.client import Client


def test_compilable():
    # will it compile an load?

    Client()
    assert True
