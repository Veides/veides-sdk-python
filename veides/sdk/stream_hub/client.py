import json
import logging
import paho.mqtt.client as paho

from veides.sdk.stream_hub.base_client import BaseClient
from veides.sdk.stream_hub.properties import AuthProperties, ConnectionProperties
from veides.sdk.stream_hub.models import Event, Trail, Timestamp


class StreamHubClient(BaseClient):
    def __init__(
            self,
            auth_properties,
            connection_properties,
            logger=None,
            mqtt_logger=None,
            log_level=logging.WARN,
            mqtt_log_level=logging.ERROR
    ):
        """
        Extends BaseClient with Veides Stream Hub features

        :param auth_properties: Auth related properties
        :type auth_properties: AuthProperties
        :param connection_properties: Properties related to Veides Stream Hub connection
        :type connection_properties: ConnectionProperties
        :param logger: Custom SDK logger
        :type logger: logging.Logger
        :param mqtt_logger: Custom MQTT lib logger
        :type mqtt_logger: logging.Logger
        :param log_level: SDK logging level
        :param mqtt_log_level: MQTT lib logging level
        """
        BaseClient.__init__(
            self,
            username=auth_properties.username,
            token=auth_properties.token,
            host=connection_properties.host,
            capath=connection_properties.capath,
            logger=logger,
            mqtt_logger=mqtt_logger,
            log_level=log_level,
            mqtt_log_level=mqtt_log_level,
        )

        self._handlers = {}

    def on_trail(self, agent, name, func):
        """
        Register a callback for the trail sent by particular agent

        :param agent: Agent's client id
        :type agent: str
        :param name: Expected trail name
        :type name: str
        :param func: Callback for trail arrival
        :type func: callable
        :return bool
        """
        self._validate_agent_client_id(agent)

        if not isinstance(name, str):
            raise TypeError('trail name should be a string')

        if len(name) == 0:
            raise ValueError('trail name should be at least 1 length')

        if not callable(func):
            raise TypeError('callback should be callable')

        return self._add_handler_and_subscribe('trail', agent, name, self._on_trail, func)

    def on_event(self, agent, name, func):
        """
        Register a callback for the event sent by particular agent

        :param agent: Agent's client id
        :type agent: str
        :param name: Expected event name
        :type name: str
        :param func: Callback for event arrival
        :type func: callable
        :return bool
        """
        self._validate_agent_client_id(agent)

        if not isinstance(name, str):
            raise TypeError('event name should be a string')

        if len(name) == 0:
            raise ValueError('event name should be at least 1 length')

        if not callable(func):
            raise TypeError('callback should be callable')

        return self._add_handler_and_subscribe('event', agent, name, self._on_event, func)

    def _on_trail(self, client, userdata, msg):
        """
        Dispatches received trail to appropriate handler

        :param client: Paho client instance
        :type client: paho.Client
        :param userdata: User-defined data
        :type: userdata: object
        :param msg: Received Paho message
        :type msg: paho.MQTTMessage
        :return void
        """
        topic_parts = msg.topic.split('/')
        agent = topic_parts[1]
        name = topic_parts[-1]
        payload = json.loads(msg.payload)
        value = payload.get('value')
        timestamp = payload.get('timestamp')

        func = self._get_handler('trail', agent, name)

        if func is not None:
            try:
                trail = Trail(name, value, Timestamp.from_string(timestamp))
                func(agent, trail)
            except (ValueError, TypeError) as e:
                self.logger.error('Could not create Trail object: %s' % str(e))

    def _on_event(self, client, userdata, msg):
        """
        Dispatches received event to appropriate handler

        :param client: Paho client instance
        :type client: paho.Client
        :param userdata: User-defined data
        :type: userdata: object
        :param msg: Received Paho message
        :type msg: paho.MQTTMessage
        :return void
        """
        topic_parts = msg.topic.split('/')
        agent = topic_parts[1]
        name = topic_parts[-1]
        payload = json.loads(msg.payload)
        message = payload.get('message')
        timestamp = payload.get('timestamp')

        func = self._get_handler('event', agent, name)

        if func is not None:
            try:
                event = Event(name, message, Timestamp.from_string(timestamp))
                func(agent, event)
            except (ValueError, TypeError) as e:
                self.logger.error('Could not create Event object: %s' % str(e))

    def _add_handler_and_subscribe(self, handler_type, agent, name, callback, handler):
        topic = 'agent/{}/{}/{}'.format(agent, handler_type, name)

        self.client.message_callback_add(topic, callback)
        self._handlers['{}_{}_{}'.format(handler_type, agent, name)] = handler

        return self._subscribe(topic, 1)

    def _get_handler(self, handler_type, agent, name):
        return self._handlers.get('{}_{}_{}'.format(handler_type, agent, name), None)

    def _validate_agent_client_id(self, client_id):
        if not isinstance(client_id, str):
            raise TypeError('agent client id should be a string')

        if len(client_id) != 32:
            raise ValueError('agent client id should be 32 length string')
