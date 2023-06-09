import os
import typing
import helpers

from sensory_cloud.initializer import Initializer, FileSystemCredentialStore

import sensory_cloud.generated.v1.management.device_pb2 as device_pb2


def enroll_device_example() -> typing.Union[device_pb2.DeviceResponse, Exception]:
    """
    Example function that uses the Initializer class to register a new device and
    create new client credentials
    """

    keychain = FileSystemCredentialStore(root_path=helpers.device_info_path)
    initializer: Initializer = Initializer(
        init_config=helpers.config_path, keychain=keychain
    )

    response: typing.Union[
        device_pb2.DeviceResponse, Exception
    ] = initializer.initialize()

    return response


if __name__ == "__main__":
    enrollment_initialization: typing.Union[
        device_pb2.DeviceResponse, Exception
    ] = enroll_device_example()
