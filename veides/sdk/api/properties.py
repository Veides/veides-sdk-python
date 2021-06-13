import os
from veides.sdk.api.exceptions import ConfigurationException


class AuthProperties:
    def __init__(self, token):
        """
        :param token: User's token
        :type token: str
        """
        self._token = token

    @property
    def token(self):
        return self._token

    @staticmethod
    def from_env():
        """
        Returns AuthProperties instance built from env variables. Required variables are:
            2. VEIDES_AUTH_USER_TOKEN: user's token

        :raises ConfigurationException: If required variables are not provided
        :return AuthProperties
        """
        token = os.getenv('VEIDES_AUTH_USER_TOKEN', None)

        if token is None:
            raise ConfigurationException("Missing 'VEIDES_AUTH_USER_TOKEN' variable in env")

        return AuthProperties(token)


class ConfigurationProperties:
    def __init__(self, base_url):
        """
        :param base_url: Veides API url
        :type base_url: str
        """
        self._base_url = base_url

    @property
    def base_url(self):
        return self._base_url

    @staticmethod
    def from_env():
        """
        Returns ConnectionProperties instance built from env variables. Required variables are:
            1. VEIDES_API_BASE_URL: Veides Api url

        :raises ConfigurationException: If required variables are not provided
        :return ConnectionProperties
        """
        base_url = os.getenv('VEIDES_API_BASE_URL', None)

        if base_url is None:
            raise ConfigurationException("Missing 'VEIDES_API_BASE_URL' variable in env")

        return ConfigurationProperties(base_url)
