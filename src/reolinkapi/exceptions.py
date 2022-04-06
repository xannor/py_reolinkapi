""" Exception """


class ReolinkError(Exception):
    """Base Error Class"""


class InvalidCredentialsError(ReolinkError):
    """Bad or missing credentials"""


class InvalidResponseError(ReolinkError):
    """Invalid or unexpected response"""
