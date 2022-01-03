import typing
from enum import Enum

from sensory_cloud.config import Config
from sensory_cloud.token_manager import ITokenManager, Metadata
from sensory_cloud.generated.v1.audio.audio_pb2_grpc import (
    AudioModelsStub,
    AudioBiometricsStub,
    AudioEventsStub,
    AudioTranscriptionsStub,
)
from sensory_cloud.generated.v1.audio.audio_pb2 import (
    GetModelsRequest,
    GetModelsResponse,
    CreateEnrollmentConfig,
    CreateEnrollmentRequest,
    CreateEnrollmentResponse,
    AudioConfig,
    ThresholdSensitivity,
    AuthenticateConfig,
    AuthenticateRequest,
    AuthenticateResponse,
    TranscribeConfig,
    TranscribeRequest,
    TranscribeResponse,
    AuthenticateRequest,
    ValidateEventConfig,
    ValidateEventRequest,
    ValidateEventResponse,
)


class AudioRequest(Enum):
    CreateEnrollmentRequest
    AuthenticateRequest
    TranscribeRequest
    ValidateEventRequest


class RequestConfig(Enum):
    CreateEnrollmentConfig
    AuthenticateConfig
    TranscribeConfig
    ValidateEventConfig


class RequestIterator:
    """
    The RequestIterator class facilitates the request streams that are sent to the 
    grpc server.  There are four possible audio request types and request configurations 
    that are given by the AudioRequest and RequestConfig enums respectively.  The first
    request sent must be a configuration request and all subsequent requests contain the audio
    content being streamed.
    """
    
    _first_request: bool = True

    def __init__(
        self,
        audio_request: AudioRequest,
        request_config: RequestConfig,
        audio_stream_iterator: typing.Iterable[bytes],
    ):
        self._audio_request = audio_request
        self._request_config = request_config
        self._audio_stream_iterator = audio_stream_iterator

    def __iter__(self):
        return self

    def __next__(self):
        if self._first_request:
            self._first_request = False
            return self._audio_request(config=self._request_config)
        else:
            audio_content = next(self._audio_stream_iterator)
            return self._audio_request(audioContent=audio_content)


class AudioService:
    """ """

    def __init__(self, config: Config, token_manager: ITokenManager):
        self._config: Config = config
        self._token_manager: ITokenManager = token_manager
        self._audio_models_client: AudioModelsStub = AudioModelsStub(config.channel)
        self._audio_biometrics_client: AudioBiometricsStub = AudioBiometricsStub(
            config.channel
        )
        self._audio_events_client: AudioEventsStub = AudioEventsStub(config.channel)
        self._audio_transcriptions_client: AudioTranscriptionsStub = (
            AudioTranscriptionsStub(config.channel)
        )

    def get_models(self) -> GetModelsResponse:
        """ """

        request: GetModelsRequest = GetModelsRequest()

        metadata: Metadata = self._token_manager.get_authorization_metadata()

        models: GetModelsResponse = self._audio_models_client.GetModels(
            request=request, metadata=metadata
        )

        return models

    def stream_enrollment(
        self,
        audio_config: AudioConfig,
        description: str,
        user_id: str,
        device_id: str,
        model_name: str,
        is_liveness_enabled: bool,
        audio_stream_iterator: typing.Iterable[bytes],
    ) -> typing.Iterable[CreateEnrollmentResponse]:
        """

        Arguments:
            audio_config: AudioConfig object
            description: String containing a description of the enrollment
            user_id: String containing the user id
            device_id: String containing the device id
            model_name: String containing the model name
            is_liveness_enabled: Boolean indicating whether or not liveness is enabled
            audio_stream_iterator: Iterator of audio bytes

        Returns:
            An iterator of CreateEnrollmentResponse objects
        """

        config: CreateEnrollmentConfig = CreateEnrollmentConfig(
            audio=audio_config,
            description=description,
            userId=user_id,
            modelName=model_name,
            deviceId=device_id,
            isLivenessEnabled=is_liveness_enabled,
        )

        request_iterator: RequestIterator = RequestIterator(
            audio_request=CreateEnrollmentRequest,
            request_config=config,
            audio_stream_iterator=audio_stream_iterator,
        )

        metadata: Metadata = self._token_manager.get_authorization_metadata()

        enrollment_stream: typing.Iterable[
            CreateEnrollmentResponse
        ] = self._audio_biometrics_client.CreateEnrollment(
            request_iterator=request_iterator, metadata=metadata
        )

        return enrollment_stream

    def stream_authenticate(
        self,
        audio_config: AudioConfig,
        enrollment_id: str,
        is_liveness_enabled: bool,
        audio_stream_iterator: typing.Iterable[bytes],
        sensitivity: ThresholdSensitivity = ThresholdSensitivity.Value("MEDIUM"),
        security: AuthenticateConfig.ThresholdSecurity = AuthenticateConfig.ThresholdSecurity.Value(
            "HIGH"
        ),
    ) -> typing.Iterable[AuthenticateResponse]:
        """

        Arguments:
            audio_config: AudioConfig object
            enrollment_id: String containing the enrollment id to authenticate on
            is_liveness_enabled: Boolean indicating whether or not liveness is enabled
            audio_stream_iterator: Iterator of audio bytes
            sensitivity: ThresholdSensitivity enum that sets the sensitivity level of the authentication
            security: AuthenticateConfig.ThresholdSecurity that sets the security level of the authentication

        Returns:
            An iterator of AuthenticateResponse objects
        """

        authenticate_config: AuthenticateConfig = AuthenticateConfig(
            audio=audio_config,
            enrollmentId=enrollment_id,
            sensitivity=sensitivity,
            security=security,
            isLivenessEnabled=is_liveness_enabled,
        )

        authenticate_stream: typing.Iterable[
            AuthenticateResponse
        ] = self._stream_authentication(
            config=authenticate_config, audio_stream_iterator=audio_stream_iterator
        )

        return authenticate_stream

    def stream_group_authenticate(
        self,
        audio_config: AudioConfig,
        enrollment_group_id: str,
        is_liveness_enabled: bool,
        audio_stream_iterator: typing.Iterable[bytes],
        sensitivity: ThresholdSensitivity = ThresholdSensitivity.Value("MEDIUM"),
        security: AuthenticateConfig.ThresholdSecurity = AuthenticateConfig.ThresholdSecurity.Value(
            "HIGH"
        ),
    ) -> typing.Iterable[AuthenticateResponse]:
        """ """

        authenticate_config: AuthenticateConfig = AuthenticateConfig(
            audio=audio_config,
            enrollmentGroupId=enrollment_group_id,
            sensitivity=sensitivity,
            security=security,
            isLivenessEnabled=is_liveness_enabled,
        )

        group_authenticate_stream: typing.Iterable[
            AuthenticateResponse
        ] = self._stream_authentication(
            config=authenticate_config, audio_stream_iterator=audio_stream_iterator
        )

        return group_authenticate_stream

    def stream_event(
        self,
        audio_config: AudioConfig,
        user_id: str,
        model_name: str,
        audio_stream_iterator: typing.Iterable[bytes],
        sensitivity: ThresholdSensitivity = ThresholdSensitivity.Value("MEDIUM"),
    ) -> typing.Iterable[ValidateEventResponse]:
        """ """

        config = ValidateEventConfig(
            audio=audio_config,
            modelName=model_name,
            userId=user_id,
            sensitivity=sensitivity,
        )

        request_iterator: RequestIterator = RequestIterator(
            audio_request=ValidateEventRequest,
            request_config=config,
            audio_stream_iterator=audio_stream_iterator,
        )

        metadata: Metadata = self._token_manager.get_authorization_metadata()

        event_stream: typing.Iterable[
            ValidateEventResponse
        ] = self._audio_events_client.ValidateEvent(
            request_iterator=request_iterator, metadata=metadata
        )

        return event_stream

    def stream_transcription(
        self,
        audio_config: AudioConfig,
        user_id: str,
        model_name: str,
        audio_stream_iterator: typing.Iterable[bytes],
    ) -> typing.Iterable[TranscribeResponse]:
        """ """

        config: TranscribeConfig = TranscribeConfig(
            audio=audio_config, modelName=model_name, userId=user_id
        )

        request_iterator: RequestIterator = RequestIterator(
            audio_request=TranscribeRequest,
            request_config=config,
            audio_stream_iterator=audio_stream_iterator,
        )

        metadata: Metadata = self._token_manager.get_authorization_metadata()

        transcription_stream: typing.Iterable[
            TranscribeResponse
        ] = self._audio_transcriptions_client.Transcribe(
            request_iterator=request_iterator, metadata=metadata
        )

        return transcription_stream

    def _stream_authentication(
        self,
        config: AuthenticateConfig,
        audio_stream_iterator: typing.Iterable[bytes],
    ) -> typing.Iterable[AuthenticateResponse]:
        """ """

        request_iterator: RequestIterator = RequestIterator(
            audio_request=AuthenticateRequest,
            request_config=config,
            audio_stream_iterator=audio_stream_iterator,
        )

        metadata: Metadata = self._token_manager.get_authorization_metadata()

        authenticate_stream: typing.Iterable[
            AuthenticateResponse
        ] = self._audio_biometrics_client.Authenticate(
            request_iterator=request_iterator, metadata=metadata
        )

        return authenticate_stream
