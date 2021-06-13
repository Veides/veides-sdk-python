from veides.sdk.api import ApiClient, AuthProperties, ConfigurationProperties
from veides.sdk.api.exceptions import MethodTimeoutException, MethodInvalidException, MethodInvokeException
import logging
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic example of Veides API client")

    parser.add_argument("-i", "--id", required=True, help="Agent's client id")
    parser.add_argument("-t", "--token", required=True, help="User's token")
    parser.add_argument("-U", "--url", required=True, help="Veides API url")

    args = parser.parse_args()

    client = ApiClient(
        configuration_properties=ConfigurationProperties(base_url=args.url),
        # If you want to provide configuration properties in environment, use below line instead
        # configuration_properties=ConfigurationProperties.from_env()
        auth_properties=AuthProperties(
            token=args.token,
        ),
        # If you want to provide auth properties in environment, use below line instead
        # auth_properties=AuthProperties.from_env()
        # Set DEBUG level to verbose mode. Level is logging.WARN by default
        log_level=logging.DEBUG
    )

    try:
        code, method_response = client.invoke_method(args.id, 'shutdown', payload={'time': 'now'}, timeout=5000)
        print(code, method_response)
    except (MethodInvalidException, MethodInvokeException, MethodTimeoutException) as e:
        print(e)
