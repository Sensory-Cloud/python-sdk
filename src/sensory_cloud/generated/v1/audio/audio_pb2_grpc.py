# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from sensory_cloud.generated.v1.audio import audio_pb2 as v1_dot_audio_dot_audio__pb2


class AudioModelsStub(object):
    """Handles the retrieval and management of audio models
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetModels = channel.unary_unary(
                '/sensory.api.v1.audio.AudioModels/GetModels',
                request_serializer=v1_dot_audio_dot_audio__pb2.GetModelsRequest.SerializeToString,
                response_deserializer=v1_dot_audio_dot_audio__pb2.GetModelsResponse.FromString,
                )


class AudioModelsServicer(object):
    """Handles the retrieval and management of audio models
    """

    def GetModels(self, request, context):
        """Get available models for enrollment and authentication
        Authorization metadata is required {"authorization": "Bearer <TOKEN>"}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AudioModelsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetModels': grpc.unary_unary_rpc_method_handler(
                    servicer.GetModels,
                    request_deserializer=v1_dot_audio_dot_audio__pb2.GetModelsRequest.FromString,
                    response_serializer=v1_dot_audio_dot_audio__pb2.GetModelsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sensory.api.v1.audio.AudioModels', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AudioModels(object):
    """Handles the retrieval and management of audio models
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
        return grpc.experimental.unary_unary(request, target, '/sensory.api.v1.audio.AudioModels/GetModels',
            v1_dot_audio_dot_audio__pb2.GetModelsRequest.SerializeToString,
            v1_dot_audio_dot_audio__pb2.GetModelsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class AudioBiometricsStub(object):
    """Handles all audio-related biometrics
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateEnrollment = channel.stream_stream(
                '/sensory.api.v1.audio.AudioBiometrics/CreateEnrollment',
                request_serializer=v1_dot_audio_dot_audio__pb2.CreateEnrollmentRequest.SerializeToString,
                response_deserializer=v1_dot_audio_dot_audio__pb2.CreateEnrollmentResponse.FromString,
                )
        self.Authenticate = channel.stream_stream(
                '/sensory.api.v1.audio.AudioBiometrics/Authenticate',
                request_serializer=v1_dot_audio_dot_audio__pb2.AuthenticateRequest.SerializeToString,
                response_deserializer=v1_dot_audio_dot_audio__pb2.AuthenticateResponse.FromString,
                )


class AudioBiometricsServicer(object):
    """Handles all audio-related biometrics
    """

    def CreateEnrollment(self, request_iterator, context):
        """Enrolls a user with a stream of audio. Streams a CreateEnrollmentResponse as the audio is processed.
        CreateEnrollment only supports biometric-enabled models
        Authorization metadata is required {"authorization": "Bearer <TOKEN>"}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Authenticate(self, request_iterator, context):
        """Authenticates a user with a stream of audio against an existing enrollment.
        Streams an AuthenticateResponse as the audio is processed.
        Authenticate only supports biometric-enabled models
        Authorization metadata is required {"authorization": "Bearer <TOKEN>"}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AudioBiometricsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateEnrollment': grpc.stream_stream_rpc_method_handler(
                    servicer.CreateEnrollment,
                    request_deserializer=v1_dot_audio_dot_audio__pb2.CreateEnrollmentRequest.FromString,
                    response_serializer=v1_dot_audio_dot_audio__pb2.CreateEnrollmentResponse.SerializeToString,
            ),
            'Authenticate': grpc.stream_stream_rpc_method_handler(
                    servicer.Authenticate,
                    request_deserializer=v1_dot_audio_dot_audio__pb2.AuthenticateRequest.FromString,
                    response_serializer=v1_dot_audio_dot_audio__pb2.AuthenticateResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sensory.api.v1.audio.AudioBiometrics', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AudioBiometrics(object):
    """Handles all audio-related biometrics
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
        return grpc.experimental.stream_stream(request_iterator, target, '/sensory.api.v1.audio.AudioBiometrics/CreateEnrollment',
            v1_dot_audio_dot_audio__pb2.CreateEnrollmentRequest.SerializeToString,
            v1_dot_audio_dot_audio__pb2.CreateEnrollmentResponse.FromString,
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
        return grpc.experimental.stream_stream(request_iterator, target, '/sensory.api.v1.audio.AudioBiometrics/Authenticate',
            v1_dot_audio_dot_audio__pb2.AuthenticateRequest.SerializeToString,
            v1_dot_audio_dot_audio__pb2.AuthenticateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class AudioEventsStub(object):
    """Handles all audio event processing
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ValidateEvent = channel.stream_stream(
                '/sensory.api.v1.audio.AudioEvents/ValidateEvent',
                request_serializer=v1_dot_audio_dot_audio__pb2.ValidateEventRequest.SerializeToString,
                response_deserializer=v1_dot_audio_dot_audio__pb2.ValidateEventResponse.FromString,
                )
        self.CreateEnrolledEvent = channel.stream_stream(
                '/sensory.api.v1.audio.AudioEvents/CreateEnrolledEvent',
                request_serializer=v1_dot_audio_dot_audio__pb2.CreateEnrolledEventRequest.SerializeToString,
                response_deserializer=v1_dot_audio_dot_audio__pb2.CreateEnrollmentResponse.FromString,
                )
        self.ValidateEnrolledEvent = channel.stream_stream(
                '/sensory.api.v1.audio.AudioEvents/ValidateEnrolledEvent',
                request_serializer=v1_dot_audio_dot_audio__pb2.ValidateEnrolledEventRequest.SerializeToString,
                response_deserializer=v1_dot_audio_dot_audio__pb2.ValidateEnrolledEventResponse.FromString,
                )


class AudioEventsServicer(object):
    """Handles all audio event processing
    """

    def ValidateEvent(self, request_iterator, context):
        """Validates a phrase or sound with a stream of audio.
        Streams a ValidateEventResponse as the audio is processed.
        Authorization metadata is required {"authorization": "Bearer <TOKEN>"}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateEnrolledEvent(self, request_iterator, context):
        """Enrolls a sound or voice. Streams a CreateEnrollmentResponse as the audio is processed.
        CreateEnrollment supports all enrollable models
        Authorization metadata is required {"authorization": "Bearer <TOKEN>"}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ValidateEnrolledEvent(self, request_iterator, context):
        """Authenticates a sound or voice. Streams a ValidateEventResponse as the audio is processed.
        ValidateEnrolledEvent supports all enrollable models
        Authorization metadata is required {"authorization": "Bearer <TOKEN>"}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AudioEventsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ValidateEvent': grpc.stream_stream_rpc_method_handler(
                    servicer.ValidateEvent,
                    request_deserializer=v1_dot_audio_dot_audio__pb2.ValidateEventRequest.FromString,
                    response_serializer=v1_dot_audio_dot_audio__pb2.ValidateEventResponse.SerializeToString,
            ),
            'CreateEnrolledEvent': grpc.stream_stream_rpc_method_handler(
                    servicer.CreateEnrolledEvent,
                    request_deserializer=v1_dot_audio_dot_audio__pb2.CreateEnrolledEventRequest.FromString,
                    response_serializer=v1_dot_audio_dot_audio__pb2.CreateEnrollmentResponse.SerializeToString,
            ),
            'ValidateEnrolledEvent': grpc.stream_stream_rpc_method_handler(
                    servicer.ValidateEnrolledEvent,
                    request_deserializer=v1_dot_audio_dot_audio__pb2.ValidateEnrolledEventRequest.FromString,
                    response_serializer=v1_dot_audio_dot_audio__pb2.ValidateEnrolledEventResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sensory.api.v1.audio.AudioEvents', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AudioEvents(object):
    """Handles all audio event processing
    """

    @staticmethod
    def ValidateEvent(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/sensory.api.v1.audio.AudioEvents/ValidateEvent',
            v1_dot_audio_dot_audio__pb2.ValidateEventRequest.SerializeToString,
            v1_dot_audio_dot_audio__pb2.ValidateEventResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CreateEnrolledEvent(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/sensory.api.v1.audio.AudioEvents/CreateEnrolledEvent',
            v1_dot_audio_dot_audio__pb2.CreateEnrolledEventRequest.SerializeToString,
            v1_dot_audio_dot_audio__pb2.CreateEnrollmentResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ValidateEnrolledEvent(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/sensory.api.v1.audio.AudioEvents/ValidateEnrolledEvent',
            v1_dot_audio_dot_audio__pb2.ValidateEnrolledEventRequest.SerializeToString,
            v1_dot_audio_dot_audio__pb2.ValidateEnrolledEventResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class AudioTranscriptionsStub(object):
    """Handles all audio transcriptions
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Transcribe = channel.stream_stream(
                '/sensory.api.v1.audio.AudioTranscriptions/Transcribe',
                request_serializer=v1_dot_audio_dot_audio__pb2.TranscribeRequest.SerializeToString,
                response_deserializer=v1_dot_audio_dot_audio__pb2.TranscribeResponse.FromString,
                )


class AudioTranscriptionsServicer(object):
    """Handles all audio transcriptions
    """

    def Transcribe(self, request_iterator, context):
        """Transcribes voice into text.
        Authorization metadata is required {"authorization": "Bearer <TOKEN>"}
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AudioTranscriptionsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Transcribe': grpc.stream_stream_rpc_method_handler(
                    servicer.Transcribe,
                    request_deserializer=v1_dot_audio_dot_audio__pb2.TranscribeRequest.FromString,
                    response_serializer=v1_dot_audio_dot_audio__pb2.TranscribeResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sensory.api.v1.audio.AudioTranscriptions', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class AudioTranscriptions(object):
    """Handles all audio transcriptions
    """

    @staticmethod
    def Transcribe(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/sensory.api.v1.audio.AudioTranscriptions/Transcribe',
            v1_dot_audio_dot_audio__pb2.TranscribeRequest.SerializeToString,
            v1_dot_audio_dot_audio__pb2.TranscribeResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)