from veides.sdk.api.base_client import BaseClient
from veides.sdk.api.exceptions import (
    MethodTimeoutException,
    MethodInvokeException,
    MethodInvalidException,
    MethodUnauthorizedException
)
import logging


class ApiClient(BaseClient):
    def __init__(
            self,
            auth_properties,
            configuration_properties,
            log_level=logging.WARN,
            logger=None
    ):
        BaseClient.__init__(
            self,
            base_url=configuration_properties.base_url,
            token=auth_properties.token,
            log_level=log_level,
            logger=logger
        )

    def invoke_method(self, agent, name, payload, timeout=30000):
        """
        Invokes a method on an agent and returns the method response (code and payload) sent by agent

        :param agent: Agent's client id
        :type agent: str
        :param name: Method name
        :type agent: str
        :param payload: Method payload to process by agent
        :type payload: dict|list|str|int|float|bool
        :param timeout: Invoked method will fail after timeout (in ms) period if agent will not send method response
        :type timeout: int
        :return: (int, dict|list|str|int|float|bool)
        """
        if not isinstance(agent, str):
            raise TypeError('agent client id should be a string')

        if len(agent) == 0:
            raise ValueError('agent client id should be at least 1 length')

        if not isinstance(name, str):
            raise TypeError('method name should be a string')

        if len(name) == 0:
            raise ValueError('method name should be at least 1 length')

        if payload is None:
            raise ValueError('payload should be one of: dictionary, list, string, integer, float, boolean')

        if not isinstance(timeout, int):
            raise TypeError('timeout should be an integer')

        if timeout < 1000:
            timeout = 1000
            self.logger.warning(
                'Provided invoke method timeout is lesser than allowed. Timeout adjusted to %d' % timeout
            )
        elif timeout > 30000:
            timeout = 30000
            self.logger.warning(
                'Provided invoke method timeout is greater than allowed. Timeout adjusted to %d' % timeout
            )

        self.logger.info('Invoking method {} on agent {}'.format(name, agent))

        response = self._post('/agents/{}/methods/{}'.format(agent, name), payload, {'timeout': timeout})

        if response.status_code == 504:
            raise MethodTimeoutException('Method {} on agent {} timeouted after {} ms'.format(name, agent, timeout))

        if response.status_code == 500:
            raise MethodInvokeException('Error occurred while invoking method {} on agent {}'.format(name, agent))

        if response.status_code == 400:
            raise MethodInvalidException(response.json().get('error'))

        if response.status_code == 403:
            raise MethodUnauthorizedException(response.json().get('error'))

        return response.status_code, response.json()
