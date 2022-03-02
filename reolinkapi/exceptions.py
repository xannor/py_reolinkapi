""" Exception """


class ReolinkError(Exception):
    """Base Error Class"""


class TimeoutError(ReolinkError):
    """Connection Timed out"""


class InvalidCredentialsError(ReolinkError):
    """Bad or missing credentials"""


class InvalidResponseError(ReolinkError):
    """Invalid or unexpected response"""
