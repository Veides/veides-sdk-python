import pytest
from paho.mqtt.client import MQTT_ERR_SUCCESS
from veides.sdk.stream_hub import StreamHubClient, AuthProperties, ConnectionProperties
from veides.sdk.stream_hub.models import TrailTimestamp


TIMESTAMP = '2021-01-01T12:00:00Z'
trail_timestamp = TrailTimestamp.from_string(TIMESTAMP)


@pytest.fixture()
def agent_client_id():
    return 'id'


@pytest.fixture()
def username():
    return 'name'


@pytest.fixture()
def token():
    return 'token'


@pytest.fixture()
def hostname():
    return 'hostname'


@pytest.fixture()
def mocked_paho_client(mocker):
    class MockedPahoClient:
        connect = mocker.stub("connect")
        disconnect = mocker.stub("disconnect")
        loop_start = mocker.stub("loop_start")
        loop_stop = mocker.stub("loop_stop")
        username_pw_set = mocker.stub("username_pw_set")
        tls_set_context = mocker.stub("tls_set_context")
        message_callback_add = mocker.stub("message_callback_add")
        publish = mocker.stub("publish")
        subscribe = mocker.stub("subscribe")

    return MockedPahoClient()


@pytest.fixture()
def connected_client(mocker, mocked_paho_client, username, token, hostname):
    mocker.patch("paho.mqtt.client.Client", return_value=mocked_paho_client)

    client = StreamHubClient(
        AuthProperties(username=username, token=token),
        ConnectionProperties(host=hostname)
    )
    client.connected.set()

    client.client.subscribe.return_value = (MQTT_ERR_SUCCESS,)

    return client


@pytest.fixture()
def not_connected_client(mocker, mocked_paho_client, username, token, hostname):
    mocker.patch("paho.mqtt.client.Client", return_value=mocked_paho_client)

    client = StreamHubClient(
        AuthProperties(username=username, token=token),
        ConnectionProperties(host=hostname)
    )

    return client
