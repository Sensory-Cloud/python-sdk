# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from sensory_cloud.generated.common import common_pb2 as common_dot_common__pb2
from sensory_cloud.generated.health import health_pb2 as health_dot_health__pb2


class HealthServiceStub(object):
    """Service for Health function
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetHealth = channel.unary_unary(
                '/sensory.api.health.HealthService/GetHealth',
                request_serializer=health_dot_health__pb2.HealthRequest.SerializeToString,
                response_deserializer=common_dot_common__pb2.ServerHealthResponse.FromString,
                )


class HealthServiceServicer(object):
    """Service for Health function
    """

    def GetHealth(self, request, context):
        """Obtain an Health and Server status information
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_HealthServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetHealth': grpc.unary_unary_rpc_method_handler(
                    servicer.GetHealth,
                    request_deserializer=health_dot_health__pb2.HealthRequest.FromString,
                    response_serializer=common_dot_common__pb2.ServerHealthResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sensory.api.health.HealthService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class HealthService(object):
    """Service for Health function
    """

    @staticmethod
    def GetHealth(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sensory.api.health.HealthService/GetHealth',
            health_dot_health__pb2.HealthRequest.SerializeToString,
            common_dot_common__pb2.ServerHealthResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
