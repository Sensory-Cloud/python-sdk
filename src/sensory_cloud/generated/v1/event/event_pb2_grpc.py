# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from sensory_cloud.generated.v1.event import event_pb2 as v1_dot_event_dot_event__pb2


class EventServiceStub(object):
    """Service to publish events to the cloud
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.PublishUsageEvents = channel.unary_unary(
                '/sensory.api.v1.event.EventService/PublishUsageEvents',
                request_serializer=v1_dot_event_dot_event__pb2.PublishUsageEventsRequest.SerializeToString,
                response_deserializer=v1_dot_event_dot_event__pb2.PublishUsageEventsResponse.FromString,
                )
        self.GetUsageEventList = channel.unary_unary(
                '/sensory.api.v1.event.EventService/GetUsageEventList',
                request_serializer=v1_dot_event_dot_event__pb2.UsageEventListRequest.SerializeToString,
                response_deserializer=v1_dot_event_dot_event__pb2.UsageEventListResponse.FromString,
                )
        self.GetUsageEventSummary = channel.unary_unary(
                '/sensory.api.v1.event.EventService/GetUsageEventSummary',
                request_serializer=v1_dot_event_dot_event__pb2.UsageEventListRequest.SerializeToString,
                response_deserializer=v1_dot_event_dot_event__pb2.UsageEventSummary.FromString,
                )


class EventServiceServicer(object):
    """Service to publish events to the cloud
    """

    def PublishUsageEvents(self, request, context):
        """Publishes a list of usage event to the cloud
        Authorization metadata is required {"authorization": "Bearer <TOKEN>"}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUsageEventList(self, request, context):
        """Obtains a list of events given the filter criteria
        Authorization metadata is required {"authorization": "Bearer <TOKEN>"}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUsageEventSummary(self, request, context):
        """Obtains a summary of events given the filter critieria
        Authorization metadata is required {"authorization": "Bearer <TOKEN>"}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_EventServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'PublishUsageEvents': grpc.unary_unary_rpc_method_handler(
                    servicer.PublishUsageEvents,
                    request_deserializer=v1_dot_event_dot_event__pb2.PublishUsageEventsRequest.FromString,
                    response_serializer=v1_dot_event_dot_event__pb2.PublishUsageEventsResponse.SerializeToString,
            ),
            'GetUsageEventList': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUsageEventList,
                    request_deserializer=v1_dot_event_dot_event__pb2.UsageEventListRequest.FromString,
                    response_serializer=v1_dot_event_dot_event__pb2.UsageEventListResponse.SerializeToString,
            ),
            'GetUsageEventSummary': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUsageEventSummary,
                    request_deserializer=v1_dot_event_dot_event__pb2.UsageEventListRequest.FromString,
                    response_serializer=v1_dot_event_dot_event__pb2.UsageEventSummary.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sensory.api.v1.event.EventService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class EventService(object):
    """Service to publish events to the cloud
    """

    @staticmethod
    def PublishUsageEvents(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sensory.api.v1.event.EventService/PublishUsageEvents',
            v1_dot_event_dot_event__pb2.PublishUsageEventsRequest.SerializeToString,
            v1_dot_event_dot_event__pb2.PublishUsageEventsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetUsageEventList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sensory.api.v1.event.EventService/GetUsageEventList',
            v1_dot_event_dot_event__pb2.UsageEventListRequest.SerializeToString,
            v1_dot_event_dot_event__pb2.UsageEventListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetUsageEventSummary(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sensory.api.v1.event.EventService/GetUsageEventSummary',
            v1_dot_event_dot_event__pb2.UsageEventListRequest.SerializeToString,
            v1_dot_event_dot_event__pb2.UsageEventSummary.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
