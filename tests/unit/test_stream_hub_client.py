import pytest
import json
from paho.mqtt.client import MQTTMessage
from tests.unit.fixtures import (
    connected_client,
    not_connected_client,
    mocked_paho_client,
    agent_client_id,
    username,
    token,
    hostname
)


def test_stream_hub_client_should_set_event_when_connected(not_connected_client, hostname):
    def side_effect(*_, **__):
        not_connected_client.client.on_connect(None, None, None, 0)

    not_connected_client.client.connect.side_effect = side_effect
    not_connected_client.connect()

    not_connected_client.client.connect.assert_called_once_with(hostname, keepalive=60, port=9001)
    not_connected_client.client.loop_start.assert_called_once()
    assert not_connected_client.is_connected() is True


def test_stream_hub_client_should_stop_loop_and_clear_event_after_disconnect(connected_client):
    def side_effect(*_, **__):
        connected_client.client.on_disconnect(None, None, 0)

    connected_client.client.disconnect.side_effect = side_effect

    connected_client.disconnect()

    connected_client.client.disconnect.assert_called_once()
    connected_client.client.loop_stop.assert_called_once()
    assert connected_client.is_connected() is False


def test_stream_hub_client_should_setup_credentials(not_connected_client, username, token):
    not_connected_client.client.username_pw_set.assert_called_once_with(username, token)


def test_stream_hub_client_should_setup_tls_context(not_connected_client):
    not_connected_client.client.tls_set_context.assert_called_once()


def test_stream_hub_client_should_use_trail_handler_when_trail_received(mocker, agent_client_id, connected_client):
    trail_name = 'some_trail'

    msg = MQTTMessage()
    msg.topic = f'agent/{agent_client_id}/trail/{trail_name}'.encode('utf-8')
    msg.payload = json.dumps({'value': 'value', 'timestamp': '2021-01-01T12:00:00Z'}).encode('utf-8')

    func = mocker.stub('some_trail_handler')

    connected_client.on_trail(agent_client_id, trail_name, func)

    connected_client._on_trail(None, None, msg)

    func.assert_called_once()


def test_stream_hub_client_should_not_use_trail_handler_when_different_trail_received(agent_client_id, mocker, connected_client):
    trail_name = 'some_trail'
    other_trail_name = 'other_trail'

    msg = MQTTMessage()
    msg.topic = f'agent/{agent_client_id}/trail/{other_trail_name}'.encode('utf-8')
    msg.payload = json.dumps({'value': 'value', 'timestamp': '2021-01-01T12:00:00Z'}).encode('utf-8')

    func = mocker.stub('some_trail_handler')

    connected_client.on_trail(agent_client_id, trail_name, func)

    connected_client._on_trail(None, None, msg)

    func.assert_not_called()


def test_stream_hub_client_should_not_use_trail_handler_when_trail_for_other_agent_received(agent_client_id, mocker, connected_client):
    trail_name = 'some_trail'
    other_agent = 'other_agent'

    msg = MQTTMessage()
    msg.topic = f'agent/{other_agent}/trail/{trail_name}'.encode('utf-8')
    msg.payload = json.dumps({'value': 'value', 'timestamp': '2021-01-01T12:00:00Z'}).encode('utf-8')

    func = mocker.stub('some_trail_handler')

    connected_client.on_trail(agent_client_id, trail_name, func)

    connected_client._on_trail(None, None, msg)

    func.assert_not_called()


def test_stream_hub_client_on_trail_should_accept_specific_parameters(agent_client_id, connected_client):
    def handler():
        pass

    agent = agent_client_id
    trail_name = 'some_trail_name'

    connected_client.on_trail(agent, trail_name, handler)


@pytest.mark.parametrize("agent,trail_name,func", [
    ('id', '', None),
    ('', 'name', lambda: None),
    ('id', {}, lambda: None),
    ({}, 'name', lambda: None),
    (123, 'name', lambda: None),
    ('id', '', lambda: None),
    ('id', 123, 123),
    ('id', '', ''),
    ('', '', ''),
    ('id', [], []),
    ('id', None, None),
    ('id', None, lambda: 1),
])
def test_stream_hub_client_on_trail_should_raise_error_when_given_invalid_parameter(agent, trail_name, func, connected_client):
    with pytest.raises(Exception):
        connected_client.on_trail(agent, trail_name, func)
