import os
from veides.sdk.stream_hub.exceptions import ConfigurationException


class AuthProperties:
    def __init__(self, username, token):
        """
        :param username: User's name
        :type username: str
        :param token: User's token
        :type token: str
        """
        self._username = username
        self._token = token

    @property
    def username(self):
        return self._username

    @property
    def token(self):
        return self._token

    @staticmethod
    def from_env():
        """
        Returns AuthProperties instance built from env variables. Required variables are:
            1. VEIDES_AUTH_USER_NAME: users's name
            2. VEIDES_AUTH_USER_TOKEN: user's token

        :raises ConfigurationException: If required variables are not provided
        :return AuthProperties
        """
        username = os.getenv('VEIDES_AUTH_USER_NAME', None)
        token = os.getenv('VEIDES_AUTH_USER_TOKEN', None)

        if username is None:
            raise ConfigurationException("Missing 'VEIDES_AUTH_USER_NAME' variable in env")

        if token is None:
            raise ConfigurationException("Missing 'VEIDES_AUTH_USER_TOKEN' variable in env")

        return AuthProperties(username, token)


class ConnectionProperties:
    def __init__(self, host, capath="/etc/ssl/certs"):
        """
        :param host: Hostname used to connect to Veides Stream Hub
        :type host: str
        :param capath: Path to certificates directory
        :type capath: str
        """
        self._host = host
        self._capath = capath

    @property
    def host(self):
        return self._host

    @property
    def capath(self):
        return self._capath

    @staticmethod
    def from_env():
        """
        Returns ConnectionProperties instance built from env variables. Required variables are:
            1. VEIDES_STREAM_HUB_CLIENT_HOST: Hostname used to connect to Veides Stream Hub

        :raises ConfigurationException: If required variables are not provided
        :return ConnectionProperties
        """
        host = os.getenv('VEIDES_STREAM_HUB_CLIENT_HOST', None)
        capath = os.getenv('VEIDES_STREAM_HUB_CLIENT_CAPATH', "/etc/ssl/certs")

        if host is None:
            raise ConfigurationException("Missing 'VEIDES_STREAM_HUB_CLIENT_HOST' variable in env")

        return ConnectionProperties(host, capath)
