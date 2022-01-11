# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from sensory_cloud.generated.v1.video import video_pb2 as v1_dot_video_dot_video__pb2


class VideoModelsStub(object):
    """Handles the retrieval and management of video models
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetModels = channel.unary_unary(
                '/sensory.api.v1.video.VideoModels/GetModels',
                request_serializer=v1_dot_video_dot_video__pb2.GetModelsRequest.SerializeToString,
                response_deserializer=v1_dot_video_dot_video__pb2.GetModelsResponse.FromString,
                )


class VideoModelsServicer(object):
    """Handles the retrieval and management of video models
    """

    def GetModels(self, request, context):
        """Get available models for enrollment and authentication
        Authorization metadata is required {"authorization": "Bearer <TOKEN>"}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_VideoModelsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetModels': grpc.unary_unary_rpc_method_handler(
                    servicer.GetModels,
                    request_deserializer=v1_dot_video_dot_video__pb2.GetModelsRequest.FromString,
                    response_serializer=v1_dot_video_dot_video__pb2.GetModelsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sensory.api.v1.video.VideoModels', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class VideoModels(object):
    """Handles the retrieval and management of video models
    """

    @staticmethod
    def GetModels(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/sensory.api.v1.video.VideoModels/GetModels',
            v1_dot_video_dot_video__pb2.GetModelsRequest.SerializeToString,
            v1_dot_video_dot_video__pb2.GetModelsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class VideoBiometricsStub(object):
    """Handles all video-related biometrics
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateEnrollment = channel.stream_stream(
                '/sensory.api.v1.video.VideoBiometrics/CreateEnrollment',
                request_serializer=v1_dot_video_dot_video__pb2.CreateEnrollmentRequest.SerializeToString,
                response_deserializer=v1_dot_video_dot_video__pb2.CreateEnrollmentResponse.FromString,
                )
        self.Authenticate = channel.stream_stream(
                '/sensory.api.v1.video.VideoBiometrics/Authenticate',
                request_serializer=v1_dot_video_dot_video__pb2.AuthenticateRequest.SerializeToString,
                response_deserializer=v1_dot_video_dot_video__pb2.AuthenticateResponse.FromString,
                )


class VideoBiometricsServicer(object):
    """Handles all video-related biometrics
    """

    def CreateEnrollment(self, request_iterator, context):
        """Enrolls a user with a stream of video. Streams a CreateEnrollmentResponse
        as the video is processed.
        Authorization metadata is required {"authorization": "Bearer <TOKEN>"}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Authenticate(self, request_iterator, context):
        """Authenticates a user with a stream of video against an existing enrollment.
        Streams an AuthenticateResponse as the video is processed.
        Authorization metadata is required {"authorization": "Bearer <TOKEN>"}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_VideoBiometricsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateEnrollment': grpc.stream_stream_rpc_method_handler(
                    servicer.CreateEnrollment,
                    request_deserializer=v1_dot_video_dot_video__pb2.CreateEnrollmentRequest.FromString,
                    response_serializer=v1_dot_video_dot_video__pb2.CreateEnrollmentResponse.SerializeToString,
            ),
            'Authenticate': grpc.stream_stream_rpc_method_handler(
                    servicer.Authenticate,
                    request_deserializer=v1_dot_video_dot_video__pb2.AuthenticateRequest.FromString,
                    response_serializer=v1_dot_video_dot_video__pb2.AuthenticateResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sensory.api.v1.video.VideoBiometrics', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class VideoBiometrics(object):
    """Handles all video-related biometrics
    """

    @staticmethod
    def CreateEnrollment(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/sensory.api.v1.video.VideoBiometrics/CreateEnrollment',
            v1_dot_video_dot_video__pb2.CreateEnrollmentRequest.SerializeToString,
            v1_dot_video_dot_video__pb2.CreateEnrollmentResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Authenticate(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/sensory.api.v1.video.VideoBiometrics/Authenticate',
            v1_dot_video_dot_video__pb2.AuthenticateRequest.SerializeToString,
            v1_dot_video_dot_video__pb2.AuthenticateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class VideoRecognitionStub(object):
    """Handles all video recognition endpoints
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ValidateLiveness = channel.stream_stream(
                '/sensory.api.v1.video.VideoRecognition/ValidateLiveness',
                request_serializer=v1_dot_video_dot_video__pb2.ValidateRecognitionRequest.SerializeToString,
                response_deserializer=v1_dot_video_dot_video__pb2.LivenessRecognitionResponse.FromString,
                )


class VideoRecognitionServicer(object):
    """Handles all video recognition endpoints
    """

    def ValidateLiveness(self, request_iterator, context):
        """Validates the liveness of a single image or stream of images.
        Streams a ValidateRecognitionResponse as the images are processed.
        Authorization metadata is required {"authorization": "Bearer <TOKEN>"}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_VideoRecognitionServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ValidateLiveness': grpc.stream_stream_rpc_method_handler(
                    servicer.ValidateLiveness,
                    request_deserializer=v1_dot_video_dot_video__pb2.ValidateRecognitionRequest.FromString,
                    response_serializer=v1_dot_video_dot_video__pb2.LivenessRecognitionResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sensory.api.v1.video.VideoRecognition', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class VideoRecognition(object):
    """Handles all video recognition endpoints
    """

    @staticmethod
    def ValidateLiveness(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/sensory.api.v1.video.VideoRecognition/ValidateLiveness',
            v1_dot_video_dot_video__pb2.ValidateRecognitionRequest.SerializeToString,
            v1_dot_video_dot_video__pb2.LivenessRecognitionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)