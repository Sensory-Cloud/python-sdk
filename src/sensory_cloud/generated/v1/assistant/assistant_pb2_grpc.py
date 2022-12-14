# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from sensory_cloud.generated.v1.assistant import assistant_pb2 as v1_dot_assistant_dot_assistant__pb2


class AssistantServiceStub(object):
    """Serivce to comunicate with an assistant
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ProcessMessage = channel.stream_stream(
                '/sensory.api.v1.assistant.AssistantService/ProcessMessage',
                request_serializer=v1_dot_assistant_dot_assistant__pb2.AssistantMessageRequest.SerializeToString,
                response_deserializer=v1_dot_assistant_dot_assistant__pb2.AssistantMessageResponse.FromString,
                )


class AssistantServiceServicer(object):
    """Serivce to comunicate with an assistant
    """

    def ProcessMessage(self, request_iterator, context):
        """Sends and process messages from a virtual assistant
        Authorization metadata is required {"authorization": "Bearer <TOKEN>"}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AssistantServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ProcessMessage': grpc.stream_stream_rpc_method_handler(
                    servicer.ProcessMessage,
                    request_deserializer=v1_dot_assistant_dot_assistant__pb2.AssistantMessageRequest.FromString,
                    response_serializer=v1_dot_assistant_dot_assistant__pb2.AssistantMessageResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sensory.api.v1.assistant.AssistantService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AssistantService(object):
    """Serivce to comunicate with an assistant
    """

    @staticmethod
    def ProcessMessage(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/sensory.api.v1.assistant.AssistantService/ProcessMessage',
            v1_dot_assistant_dot_assistant__pb2.AssistantMessageRequest.SerializeToString,
            v1_dot_assistant_dot_assistant__pb2.AssistantMessageResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)