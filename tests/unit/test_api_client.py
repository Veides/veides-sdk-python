import pytest
from veides.sdk.api import __version__
from veides.sdk.api.exceptions import (
    MethodInvalidException,
    MethodInvokeException,
    MethodTimeoutException,
    MethodUnauthorizedException
)
from tests.unit.fixtures import (
    api_client,
    agent_client_id,
    token,
    hostname
)


def test_api_client_should_invoke_method(agent_client_id, token, api_client, hostname):
    method_name = 'some_method'
    payload = []

    class MockedMethodResponse:
        status_code = 200

        def json(self):
            return dict()

    expected_response = MockedMethodResponse()

    api_client.http_client.post.return_value = expected_response

    code, response = api_client.invoke_method(agent_client_id, method_name, payload)

    assert code == expected_response.status_code
    assert response == expected_response.json()
    api_client.http_client.post.assert_called_once_with(
        '{}/v1/agents/{}/methods/some_method'.format(hostname, agent_client_id),
        json=payload,
        params={'timeout': 30000},
        headers={
            'Authorization': 'Token {}'.format(token),
            'User-Agent': 'Veides-SDK-ApiClientV1/{}/Python'.format(__version__)
        }
    )


@pytest.mark.parametrize("agent,method_name,payload,timeout", [
    ('id', 1, {}, 5000),
    (1, 'name', {}, 5000),
    ('id', 'name', {}, 'invalid_timeout'),
])
def test_api_client_should_raise_type_error_when_given_invalid_invoke_method_parameters(
    agent,
    method_name,
    payload,
    timeout,
    api_client
):
    with pytest.raises(TypeError):
        api_client.invoke_method(agent, method_name, payload, timeout)


@pytest.mark.parametrize("agent,method_name,payload,timeout", [
    ('', 'method', {}, 5000),
    ('id', '', {}, 5000),
    ('id', 'method', None, 5000),
])
def test_api_client_should_raise_value_error_when_given_invalid_invoke_method_parameter_values(
    agent,
    method_name,
    payload,
    timeout,
    api_client
):
    with pytest.raises(ValueError):
        api_client.invoke_method(agent, method_name, payload, timeout)


@pytest.mark.parametrize("response_code,expected_error", [
    (500, MethodInvokeException),
    (504, MethodTimeoutException),
    (400, MethodInvalidException),
    (403, MethodUnauthorizedException)
])
def test_api_client_should_raise_proper_error_based_on_response_code(
    response_code,
    expected_error,
    api_client,
    agent_client_id
):
    method_name = 'some_method'
    payload = []

    class MockedMethodResponse:
        status_code = response_code

        def json(self):
            return dict()

    expected_response = MockedMethodResponse()

    api_client.http_client.post.return_value = expected_response

    with pytest.raises(expected_error):
        api_client.invoke_method(agent_client_id, method_name, payload)


@pytest.mark.parametrize("response_code,expected_error", [
    (400, MethodInvalidException),
    (403, MethodUnauthorizedException)
])
def test_api_client_should_use_error_on_invoke_method_when_client_error_occurred(
    response_code,
    expected_error,
    api_client,
    agent_client_id
):
    method_name = 'some_method'
    payload = []
    error = 'some error'

    class MockedMethodResponse:
        status_code = response_code

        def json(self):
            return dict(error=error)

    expected_response = MockedMethodResponse()

    api_client.http_client.post.return_value = expected_response

    with pytest.raises(expected_error, match=error):
        api_client.invoke_method(agent_client_id, method_name, payload)
