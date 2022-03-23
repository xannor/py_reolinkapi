"""Manual tests for discovery and probing (do not run automated)"""

import logging
import os
from reolinkapi.const import DEFAULT_PASSWORD, DEFAULT_USERNAME

from reolinkapi.rest import Client
from reolinkapi.rest.connection import Encryption

from .test_encrypt import EncryptTestRig


async def test_manual(caplog):
    """manual code test"""

    caplog.set_level(logging.DEBUG)
    client = EncryptTestRig(
        AUTH_HEADER=os.environ.get("DEV_AUTH", None),
        CNONCE=(lambda: os.environ["DEV_CNONCE"])
        if "DEV_CNONCE" in os.environ
        else None,
        TOKEN=os.environ.get("DEV_TOKEN", None),
    )

    # await client.connect(os.environ.get("DEV_IP", "localhost"))
    # assert await client.login(
    #    os.environ.get("DEV_USER", DEFAULT_USERNAME),
    #    os.environ.get("DEV_PASS", DEFAULT_PASSWORD),
    # )
    client.create_cipher(os.environ["DEV_AES_KEY"], 55, 32)
    enc = "CtXbKgzX1WpIZ0ZREX++8ELcn6DKQAhR/Stnwhf4Ce0y0c+aRllshzUkXEvQDxP2fTJgPWvO3Nm6itJByzvV0X2xKudB0cYmuUTNlkv037uX4Iolf0DCOxuS/JjRaWdh4Ub7n6mIi72JrSbP9QAtKSyI5DKi5KiiOFbSjyjQlLKCaGZ4WaqrE3FYqWrGJ56atSx2WTIRBrkMzfdoA3W2oybd7SnJLgp1aOfFEvY001BUqgVUvSykxgOuunu4Ov4wzMfOygTM5TX87aWxWD8SJ0Ko2joiYGsCYYFnnIdFXj210KxElDGLlzMkeML8QchtN4Wt82+VeSwWsj1rpbobdg=="
    result = client.decrypt(enc)
    data = client.encrypt(result)
    # (_, data) = client.query_data_by_count(22)
    assert data == enc

    # await client.disconnect()


async def test_manual_live(caplog):
    """manual code test (live)"""

    caplog.set_level(logging.DEBUG)
    client = Client()
    await client.connect(
        os.environ.get("DEV_IP", "localhost"), encryption=Encryption.AES
    )
    assert await client.login(
        os.environ.get("DEV_USER", DEFAULT_USERNAME),
        os.environ.get("DEV_PASS", DEFAULT_PASSWORD),
    )
    result = await client.get_ability()

    await client.disconnect()

    assert False
