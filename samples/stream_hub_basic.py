from veides.sdk.stream_hub import StreamHubClient, AuthProperties, ConnectionProperties
from time import sleep
import logging
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic example of connecting to Veides Stream Hub")

    parser.add_argument("-u", "--username", required=True, help="User's name")
    parser.add_argument("-t", "--token", required=True, help="User's token")
    parser.add_argument("-i", "--id", required=True, help="Agent's client id")
    parser.add_argument("-H", "--host", required=True, help="Host to connect to")

    args = parser.parse_args()

    client = StreamHubClient(
        connection_properties=ConnectionProperties(host=args.host),
        # If you want to provide connection properties in environment, use below line instead
        # connection_properties=ConnectionProperties.from_env()
        auth_properties=AuthProperties(
            username=args.username,
            token=args.token,
        ),
        # If you want to provide auth properties in environment, use below line instead
        # auth_properties=AuthProperties.from_env()
        # Set DEBUG level to see received and sent data. Level is logging.WARN by default
        log_level=logging.DEBUG
    )

    client.connect()

    def on_trail(agent, trail):
        print(agent, trail)

    # Set a handler for trail
    client.on_trail(args.id, 'uptime', on_trail)

    finish = False

    while not finish:
        try:
            sleep(1)
        except KeyboardInterrupt:
            finish = True
            pass

    client.disconnect()
