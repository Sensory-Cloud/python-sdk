# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from sensory_cloud.generated.v1.management import device_pb2 as v1_dot_management_dot_device__pb2


class DeviceServiceStub(object):
    """Service to manage Devices in the database
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.EnrollDevice = channel.unary_unary(
                '/sensory.api.v1.management.DeviceService/EnrollDevice',
                request_serializer=v1_dot_management_dot_device__pb2.EnrollDeviceRequest.SerializeToString,
                response_deserializer=v1_dot_management_dot_device__pb2.DeviceResponse.FromString,
                )
        self.GetWhoAmI = channel.unary_unary(
                '/sensory.api.v1.management.DeviceService/GetWhoAmI',
                request_serializer=v1_dot_management_dot_device__pb2.DeviceGetWhoAmIRequest.SerializeToString,
                response_deserializer=v1_dot_management_dot_device__pb2.DeviceResponse.FromString,
                )


class DeviceServiceServicer(object):
    """Service to manage Devices in the database
    """

    def EnrollDevice(self, request, context):
        """Create a new device in the database
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetWhoAmI(self, request, context):
        """Allows a device to fetch information about itself
        Authorization metadata is required {"authorization": "Bearer <TOKEN>"}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DeviceServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'EnrollDevice': grpc.unary_unary_rpc_method_handler(
                    servicer.EnrollDevice,
                    request_deserializer=v1_dot_management_dot_device__pb2.EnrollDeviceRequest.FromString,
                    response_serializer=v1_dot_management_dot_device__pb2.DeviceResponse.SerializeToString,
            ),
            'GetWhoAmI': grpc.unary_unary_rpc_method_handler(
                    servicer.GetWhoAmI,
                    request_deserializer=v1_dot_management_dot_device__pb2.DeviceGetWhoAmIRequest.FromString,
                    response_serializer=v1_dot_management_dot_device__pb2.DeviceResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sensory.api.v1.management.DeviceService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DeviceService(object):
    """Service to manage Devices in the database
    """

    @staticmethod
    def EnrollDevice(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sensory.api.v1.management.DeviceService/EnrollDevice',
            v1_dot_management_dot_device__pb2.EnrollDeviceRequest.SerializeToString,
            v1_dot_management_dot_device__pb2.DeviceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetWhoAmI(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sensory.api.v1.management.DeviceService/GetWhoAmI',
            v1_dot_management_dot_device__pb2.DeviceGetWhoAmIRequest.SerializeToString,
            v1_dot_management_dot_device__pb2.DeviceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)