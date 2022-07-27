import typing
from helpers import config_path

from sensory_cloud.initializer import Initializer

import sensory_cloud.generated.v1.management.device_pb2 as device_pb2


def enroll_device_example() -> typing.Union[device_pb2.DeviceResponse, Exception]:
    """
    Example function that uses the Initializer class to register a new device and
    create new client credentials
    """

    initializer: Initializer = Initializer(init_config=config_path)

    response: typing.Union[
        device_pb2.DeviceResponse, Exception
    ] = initializer.initialize()

    return response


if __name__ == "__main__":
    enrollment_initialization: typing.Union[
        device_pb2.DeviceResponse, Exception
    ] = enroll_device_example()
