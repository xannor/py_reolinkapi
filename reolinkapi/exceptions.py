""" Exception """


class ReolinkException(Exception):
    """Base Error Class"""


class InvalidCredentials(ReolinkException):
    """Bad or missing credentials"""


class InvalidResponse(ReolinkException):
    """Invalid or unexpected response"""
