import json
import uuid

import helpers

import sensory_cloud.generated.v1.management.device_pb2 as device_pb2

from sensory_cloud.config import Config
from sensory_cloud.services.crypto_service import CryptoService
from sensory_cloud.services.oauth_service import OauthService

from secure_credential_store_example import SecureCredentialStore



def set_client_credentials(environment_config: dict) -> None:
    """
    Once the configuration parameters have been read from the config.json file into the
    environment_config dictionary, the next step is to set the client_id and client_secret parameters.
    The client_id will be set to a random uuid and the client_secret will be set to a secure random
    string with 24 characters using the Sensory Cloud CryptoService.

    Arguments:
        environment_config: Dictionary containing configuration arguments
    """

    environment_config["client_id"] = str(uuid.uuid4())
    environment_config["client_secret"] = CryptoService().get_secure_random_string(
        length=24
    )


def register_device(environment_config: dict) -> device_pb2.DeviceResponse:
    """
    Now that the client credentials are set, the device can be registered.  The device is
    registered by instantiating an OauthService object and using the register() method.
    The OauthService requires a Config object and an ISecureCredentialStore object to be constructed.
    Once the register method is called, a DeviceResponse object will be returned.

    NOTE: If you try and register a device with a device_id that already exists, the registration will fail.

    Arguments:
        environment_config: Dictionary containing configuration arguments

    Returns:
        A DeviceResponse object indicating whether or not the device registration was successful
    """

    config: Config = Config(
        fully_qualified_domain_name=environment_config["fully_qualified_domain_name"],
        tenant_id=environment_config["tenant_id"],
    )
    config.connect()

    credential_store: SecureCredentialStore = SecureCredentialStore(
        client_id=environment_config["client_id"],
        client_secret=environment_config["client_secret"],
    )

    oauth_service: OauthService = OauthService(
        config=config, secure_credential_store=credential_store
    )

    device_response: device_pb2.DeviceResponse = oauth_service.register(
        device_id=environment_config["device_id"],
        device_name=environment_config["device_name"],
        credential=environment_config["tenant_secret"],
    )

    return device_response


def save_environment_config(environment_config: dict) -> None:
    """
    Once the device has been successfully registered the client_id and client_secret
    need to be saved to the configuration file so they can be accessed in the examples
    of other Sensory Cloud services.

    Arguments:
        environment_config: Dictionary containing configuration arguments
    """

    with open(helpers.config_path, "w") as config_file:
        json.dump(environment_config, config_file, indent=4)


def run_registration() -> device_pb2.DeviceResponse:
    """
    Main method that reads in the inital configuration parameters (fully_qualified_domain_name,
    tenant_id, tenant_secret, device_id, and device_name), sets the client_id and client_secret
    config parameters, registers the device and then saves the new client credentials to config.json.

    Returns:
        A DeviceResponse object indicating whether or not the device registration was successful
    """

    set_client_credentials(helpers.environment_config)
    device_response: device_pb2.DeviceResponse = register_device(helpers.environment_config)
    save_environment_config(helpers.environment_config)

    return device_response


if __name__ == "__main__":
    device_response = run_registration()
