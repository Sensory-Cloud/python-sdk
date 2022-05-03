import json
import uuid

import helpers

import sensory_cloud.generated.v1.management.device_pb2 as device_pb2

from sensory_cloud.services.crypto_service import CryptoService
from sensory_cloud.services.oauth_service import OauthService


def set_client_credentials() -> None:
    """
    Once the configuration parameters have been read from the config.json file into the
    environment_config dictionary, the next step is to set the client_id and client_secret parameters.
    The client_id will be set to a random uuid and the client_secret will be set to a secure random
    string with 24 characters using the Sensory Cloud CryptoService.
    """

    if (
        helpers.environment_config["client_id"] == ""
        and helpers.environment_config["client_secret"] == ""
    ):
        print("Creating new client credentials..")
        helpers.environment_config["client_id"] = str(uuid.uuid4())
        helpers.environment_config[
            "client_secret"
        ] = CryptoService().get_secure_random_string(length=24)
    else:
        print("Client credentials already exist in config.json.")
        print("Clear client credentials from config.json to generate new ones.")


def check_device_is_registered() -> bool:
    """
    Attempting to register a device id for a given pair of client id and client secret
    will throw an error.  This function uses the OauthService.get_who_am_i method
    to check if the device id set in config.json has already been set and returns a boolean
    denoting whether or not that is true.

    Returns:
        A boolean denoting whether or not the device id set in the environment_config dictionary
        has already been registered
    """

    oauth_service: OauthService = helpers.get_oauth_service()

    try:
        device_response: device_pb2.DeviceResponse = oauth_service.get_who_am_i()
        registered: bool = (
            helpers.environment_config["device_id"] == device_response.deviceId
        )
    except Exception as e:
        registered: bool = False

    return registered


def save_environment_config() -> None:
    """
    Once the device has been successfully registered the client_id and client_secret
    need to be saved to the configuration file so they can be accessed in the examples
    of other Sensory Cloud services.
    """

    with open(helpers.config_path, "w") as config_file:
        json.dump(helpers.environment_config, config_file, indent=4)


def register_device() -> device_pb2.DeviceResponse:
    """
    Now that the client credentials are set, the device can be registered.  The device is
    registered by instantiating an OauthService object and using the register() method.
    The OauthService requires a Config object and an ISecureCredentialStore object to be constructed.
    Once the register method is called, a DeviceResponse object will be returned.

    NOTE: This function will check if the device id set in config.json has already been registered.
    If it has, then the DeviceResponse for the existing registered device will be returned.
    Otherwise, the registration will proceed and the DeviceResponse for the new registration will
    be returned.

    Returns:
        A DeviceResponse object indicating whether or not the device registration was successful
    """

    oauth_service: OauthService = helpers.get_oauth_service()

    if check_device_is_registered():
        print(
            f"Registration already exists for device_id = {helpers.environment_config['device_id']}"
        )
        device_response: device_pb2.DeviceResponse = oauth_service.get_who_am_i()
    else:
        print(f"Registering device_id = {helpers.environment_config['device_id']}")
        device_response: device_pb2.DeviceResponse = oauth_service.register(
            device_id=helpers.environment_config["device_id"],
            device_name=helpers.environment_config["device_name"],
            credential=helpers.environment_config["tenant_secret"],
        )
        save_environment_config()

    return device_response


def run_registration() -> device_pb2.DeviceResponse:
    """
    Main method that reads in the inital configuration parameters (fully_qualified_domain_name,
    tenant_id, tenant_secret, device_id, and device_name), sets the client_id and client_secret
    config parameters, registers the device and then saves the new client credentials to config.json.

    Returns:
        A DeviceResponse object indicating whether or not the device registration was successful
    """

    set_client_credentials()
    device_response: device_pb2.DeviceResponse = register_device()

    return device_response


if __name__ == "__main__":
    device_response = run_registration()
