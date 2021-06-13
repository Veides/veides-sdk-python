import requests
import logging
from veides.sdk.api import __version__ as api_client_version


class BaseClient(object):
    def __init__(self, base_url, token, log_level, logger=None, version='v1'):
        self.http_client = requests

        self._base_url = '{}/{}'.format(base_url, version)
        self._token = token
        self._base_headers = {
            'User-Agent': 'Veides-SDK-ApiClient{}/{}/Python'.format(version.upper(), api_client_version)
        }

        if logger is None:
            self.logger = self._build_logger(self.__module__ + "." + self.__class__.__name__, log_level)
        else:
            self.logger = logger

    def _post(self, uri, payload, params):
        url = self._base_url + uri

        return self.http_client.post(url, json=payload, params=params, headers={
            'Authorization': 'Token {}'.format(self._token),
            **self._base_headers
        })

    def _build_logger(self, name, log_level):
        logger = logging.getLogger(name)
        logger.handlers = []
        logger.setLevel(log_level)

        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(name)s [%(levelname)s] %(message)s")
        )

        logger.addHandler(handler)

        return logger
