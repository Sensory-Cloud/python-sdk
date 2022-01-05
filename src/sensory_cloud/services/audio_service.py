import typing
from enum import Enum

from sensory_cloud.config import Config
from sensory_cloud.generated.v1 import audio
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
    CreateEnrollmentEventConfig,
    CreateEnrolledEventRequest,
    ValidateEnrolledEventResponse,
    ValidateEnrolledEventConfig,
    ValidateEnrolledEventRequest,
)


class AudioRequest(Enum):
    CreateEnrollmentRequest
    AuthenticateRequest
    TranscribeRequest
    ValidateEventRequest
    CreateEnrolledEventRequest
    ValidateEnrolledEventRequest


class RequestConfig(Enum):
    CreateEnrollmentConfig
    AuthenticateConfig
    TranscribeConfig
    ValidateEventConfig
    CreateEnrollmentEventConfig


class RequestIterator:
    """
    The RequestIterator class facilitates the request streams that are sent to the
    grpc server.  There are six possible audio request types and and five request configurations
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
        """
        Constructor method for the RequestIterator class

        Arguments:
            audio_request: AudioRequest enum denoting which type of request is being sent
            request_config: RequestConfig enum containing the initial request configuration
            audio_stream_iterator: Iterator containing audio bytes
        """

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
    """ 
    Class that handles all audio requests to Sensory Cloud
    """

    def __init__(self, config: Config, token_manager: ITokenManager):
        """
        Constructor method for the AudioService class

        Arguments:
            config: Config object containing the relevant grpc connection information
            token_manager: ITokenManager object that generates and returns JWT metadata
        """

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
        """ 
        Method that fetches all the audio models supported by your instance of Sensory Cloud.

        Returns:
            A GetModelsResponse containing information about all audio models
        """

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
        Stream audio to Sensory Cloud as a means for user enrollment.
        Only biometric-typed models are supported by the method.

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
        Authenticate against an existing audio enrollment in Sensory Cloud.
        Only biometric-typed models are supported by the method.

        Arguments:
            audio_config: AudioConfig object
            enrollment_id: String containing the enrollment id to authenticate on
            is_liveness_enabled: Boolean indicating whether or not liveness is enabled
            audio_stream_iterator: Iterator of audio bytes
            sensitivity: ThresholdSensitivity enum that sets the sensitivity level of the authentication
                default = ThresholdSensitivity.Value("MEDIUM")
            security: AuthenticateConfig.ThresholdSecurity that sets the security level of the authentication
                default = AuthenticateConfig.ThresholdSecurity.Value("HIGH")

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
        """ 
        Authenticate against an existing audio enrollment in Sensory Cloud.

        Arguments:
            audio_config: AudioConfig object
            enrollment_group_id: String containing the enrollment group id to authenticate on
            is_liveness_enabled: Boolean indicating whether or not liveness is enabled
            audio_stream_iterator: Iterator of audio bytes
            sensitivity: ThresholdSensitivity enum that sets the sensitivity level of the authentication
                default = ThresholdSensitivity.Value("MEDIUM")
            security: AuthenticateConfig.ThresholdSecurity that sets the security level of the authentication
                default = AuthenticateConfig.ThresholdSecurity.Value("HIGH")

        Returns:
            An iterator of AuthenticateResponse objects
        """

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
        """ 
        Stream audio to Sensory Cloud in order to recognize a specific phrase or sound

        Arguments:
            audio_config: AudioConfig object
            user_id: String containing the user id
            model_name: String containing the name of the model to be used
            audio_stream_iterator: Iterator of audio bytes
            sensitivity: ThresholdSensitivity enum that sets the sensitivity level of the authentication
                default = ThresholdSensitivity.Value("MEDIUM")

        Returns:
            An iterator of ValidateEventResponse objects
        """

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

    def stream_create_enrolled_event(
        self,
        audio_config: AudioConfig,
        description: str,
        user_id: str,
        model_name: str,
        audio_stream_iterator: typing.Iterable[bytes],
    ) -> typing.Iterable[CreateEnrollmentResponse]:
        """
        Stream audio to Sensory Cloud as a means for audio enrollment.
        This method is similar to StreamEnrollment, but does not have the same
        time limits or model type restrictions.
        Biometric model types are not supported by this function.
        This endpoint cannot be used to establish device trust.

        Arguments:
            audio_config: AudioConfig object
            description: String containing a description of this enrollment. 
                Useful if a user could have multiple enrollments, as it helps differentiate between them.
            user_id: String containing the user id
            model_name: String containing the name of the model to be used
            audio_stream_iterator: Iterator of audio bytes

        Returns:
            An iterator of CreateEnrollmentResponse objects
        """

        config: CreateEnrollmentEventConfig = CreateEnrollmentEventConfig(
            audio=audio_config,
            userId=user_id,
            modelName=model_name,
            description=description,
        )

        request_iterator: RequestIterator = RequestIterator(
            audio_request=CreateEnrolledEventRequest,
            request_config=config,
            audio_stream_iterator=audio_stream_iterator,
        )

        metadata: Metadata = self._token_manager.get_authorization_metadata()

        enrollment_stream: typing.Iterable[
            CreateEnrollmentResponse
        ] = self._audio_events_client.CreateEnrolledEvent(
            request_iterator=request_iterator, metadata=metadata
        )

        return enrollment_stream

    def stream_validate_enrolled_event(
        self,
        audio_config: AudioConfig,
        enrollment_id: str,
        audio_stream_iterator: typing.Iterable[bytes],
        sensitivity: ThresholdSensitivity = ThresholdSensitivity.Value("MEDIUM"),
    ) -> typing.Iterable[ValidateEnrolledEventResponse]:
        """
        Validate an existing event enrollment in Sensory Cloud.
        This method is similar to Authenticate, but does not have the same
        time limits or model type restrictions. Additionally, the server will
        never close the stream, and thus a client may validate an enrolled sound
        as many times as they'd like.
        Any model types are supported by this function.
        This endpoint cannot be used to establish device trust.

        Arguments:
            audio_config: AudioConfig object
            enrollment_id: String containing the enrollment id
            audio_stream_iterator: Iterator of audio bytes
            sensitivity: ThresholdSensitivity enum that sets the sensitivity level of the authentication
                default = ThresholdSensitivity.Value("MEDIUM")

        Returns:
            An iterator of ValidateEnrolledEventResponse objects
        """

        config = ValidateEnrolledEventConfig(
            audio=audio_config,
            enrollmentId=enrollment_id,
            sensitivity=sensitivity,
        )

        validate_enrolled_event_stream: typing.Iterable[
            ValidateEnrolledEventResponse
        ] = self._stream_event_validation(
            config=config, audio_stream_iterator=audio_stream_iterator
        )

        return validate_enrolled_event_stream

    def stream_group_validate_enrolled_event(
        self,
        audio_config: AudioConfig,
        enrollment_group_id: str,
        audio_stream_iterator: typing.Iterable[bytes],
        sensitivity: ThresholdSensitivity = ThresholdSensitivity.Value("MEDIUM"),
    ) -> typing.Iterable[ValidateEnrolledEventResponse]:
        """
        Validate an existing groupd of events in Sensory Cloud.
        This method is similar to GroupAuthenticate, but does not have the same
        time limits or model type restrictions. Additionally, the server will
        never close the stream, and thus a client may validate an enrolled group
        as many times as they'd like.
        Any model types are supported by this function.
        This endpoint cannot be used to establish device trust.

        Arguments:
            audio_config: AudioConfig object
            enrollment_group_id: String containing the enrollment group id
            audio_stream_iterator: Iterator of audio bytes
            sensitivity: ThresholdSensitivity enum that sets the sensitivity level of the authentication
                default = ThresholdSensitivity.Value("MEDIUM")

        Returns:
            An iterator of ValidateEnrolledEventResponse objects
        """

        config = ValidateEnrolledEventConfig(
            audio=audio_config,
            enrollmentGroupId=enrollment_group_id,
            sensitivity=sensitivity,
        )

        validate_enrolled_event_stream: typing.Iterable[
            ValidateEnrolledEventResponse
        ] = self._stream_event_validation(
            config=config, audio_stream_iterator=audio_stream_iterator
        )

        return validate_enrolled_event_stream

    def stream_transcription(
        self,
        audio_config: AudioConfig,
        user_id: str,
        model_name: str,
        audio_stream_iterator: typing.Iterable[bytes],
    ) -> typing.Iterable[TranscribeResponse]:
        """
        Stream audio to Sensory Cloud in order to transcribe spoken words

        Arguments:
            audio_config: AudioConfig object
            user_id: String containing the user id
            model_name: String containing the name of the model to be used
            audio_stream_iterator: Iterator of audio bytes

        Returns:
            An iterator of TranscribeResponse objects
        """

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
        """
        Private method behind the public authentication methods

        Arguments:
            config: AuthenticateConfig object containing authentication configuration parameters

        Returns:
            An iterator of AuthenticateResponse objects
        """

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

    def _stream_event_validation(
        self,
        config: ValidateEnrolledEventConfig,
        audio_stream_iterator: typing.Iterable[bytes],
    ) -> typing.Iterable[ValidateEnrolledEventResponse]:
        """
        Private method behind the public event validation methods

        Arguments:
            config: ValidateEnrolledEventConfig object containing enrolled event configuration parameters

        Returns:
            An iterator of ValidateEnrolledEventResponse objects
        """

        request_iterator: RequestIterator = RequestIterator(
            audio_request=ValidateEnrolledEventRequest,
            request_config=config,
            audio_stream_iterator=audio_stream_iterator,
        )

        metadata: Metadata = self._token_manager.get_authorization_metadata()

        validate_enrolled_event_stream: typing.Iterable[
            ValidateEnrolledEventResponse
        ] = self._audio_events_client.ValidateEnrolledEvent(
            request_iterator=request_iterator, metadata=metadata
        )

        return validate_enrolled_event_stream
