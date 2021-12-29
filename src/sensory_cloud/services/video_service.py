import grpc
import typing
from enum import Enum

from sensory_cloud.config import Config
from sensory_cloud.token_manager import ITokenManager, Metadata
from sensory_cloud.generated.v1.video.video_pb2_grpc import (
    VideoModelsStub,
    VideoBiometricsStub,
    VideoRecognitionStub,
)
from sensory_cloud.generated.v1.video.video_pb2 import (
    CreateEnrollmentResponse,
    GetModelsRequest,
    GetModelsResponse,
    CreateEnrollmentConfig,
    CreateEnrollmentRequest,
    AuthenticateConfig,
    AuthenticateRequest,
    AuthenticateResponse,
    LivenessRecognitionResponse,
    RecognitionThreshold,
    ValidateRecognitionConfig,
    ValidateRecognitionRequest,
)


class VideoRequest(Enum):
    CreateEnrollmentRequest
    AuthenticateRequest
    ValidateRecognitionRequest


class RequestConfig(Enum):
    CreateEnrollmentConfig
    AuthenticateConfig
    ValidateRecognitionConfig


class RequestIterator:
    first_request: bool = True

    def __init__(
        self,
        video_request: VideoRequest,
        request_config: RequestConfig,
        video_stream_iterator: typing.Iterable[bytes],
    ):
        self.video_request = video_request
        self.request_config = request_config
        self.video_stream_iterator = video_stream_iterator

    def __iter__(self):
        return self

    def __next__(self):
        if self.first_request:
            self.first_request = False
            return self.video_request(config=self.request_config)
        else:
            return self.video_request(imageContent=next(self.video_stream_iterator))


class VideoService:
    def __init__(self, config: Config, token_manager: ITokenManager):
        self._config: Config = config
        self._token_manager: ITokenManager = token_manager
        self._video_models_client: VideoModelsStub = VideoModelsStub(config.channel)
        self._video_biometrics_client: VideoBiometricsStub = VideoBiometricsStub(
            config.channel
        )
        self._video_recognition_client: VideoRecognitionStub = VideoRecognitionStub(
            config.channel
        )

    def get_models(self) -> GetModelsResponse:
        metadata: Metadata = self._token_manager.get_authorization_metadata()
        request: GetModelsRequest = GetModelsRequest()

        return self._video_models_client.GetModels(request=request, metadata=metadata)

    def stream_enrollment(
        self,
        description: str,
        user_id: str,
        model_name: str,
        device_id: str,
        is_liveness_enabled: bool,
        video_stream_iterator: typing.Iterable[bytes],
        threshold: RecognitionThreshold = RecognitionThreshold.Value("HIGH"),
    ) -> typing.Iterable[CreateEnrollmentResponse]:

        config: CreateEnrollmentConfig = CreateEnrollmentConfig(
            description=description,
            userId=user_id,
            deviceId=device_id,
            modelName=model_name,
            isLivenessEnabled=is_liveness_enabled,
            livenessThreshold=threshold,
        )

        request_iterator: RequestIterator = RequestIterator(
            video_request=CreateEnrollmentRequest,
            request_config=config,
            video_stream_iterator=video_stream_iterator,
        )

        metadata: Metadata = self._token_manager.get_authorization_metadata()

        enrollment_stream: typing.Iterable[
            CreateEnrollmentResponse
        ] = self._video_biometrics_client.CreateEnrollment(
            request_iterator=request_iterator, metadata=metadata
        )

        return enrollment_stream

    def stream_authentication(
        self,
        enrollment_id: str,
        is_liveness_enabled: bool,
        video_stream_iterator: typing.Iterable[bytes],
        threshold: RecognitionThreshold = RecognitionThreshold.Value("HIGH"),
    ) -> typing.Iterable[AuthenticateResponse]:

        config: AuthenticateConfig = AuthenticateConfig(
            enrollmentId=enrollment_id,
            isLivenessEnabled=is_liveness_enabled,
            livenessThreshold=threshold,
        )

        request_iterator: RequestIterator = RequestIterator(
            video_request=AuthenticateRequest,
            request_config=config,
            video_stream_iterator=video_stream_iterator,
        )

        metadata: Metadata = self._token_manager.get_authorization_metadata()

        authenticate_stream: typing.Iterable[
            AuthenticateResponse
        ] = self._video_biometrics_client.Authenticate(
            request_iterator=request_iterator, metadata=metadata
        )

        return authenticate_stream

    def stream_liveness_recognition(
        self,
        user_id: str,
        model_name: str,
        video_stream_iterator: typing.Iterable[bytes],
        threshold: RecognitionThreshold = RecognitionThreshold.Value("HIGH"),
    ) -> typing.Iterable[LivenessRecognitionResponse]:

        config: ValidateRecognitionConfig = ValidateRecognitionConfig(
            userId=user_id, modelName=model_name, threshold=threshold
        )

        request_iterator: RequestIterator = RequestIterator(
            video_request=ValidateRecognitionRequest,
            request_config=config,
            video_stream_iterator=video_stream_iterator,
        )

        metadata: Metadata = self._token_manager.get_authorization_metadata()

        recognition_stream: typing.Iterable[
            LivenessRecognitionResponse
        ] = self._video_recognition_client.ValidateLiveness(
            request_iterator=request_iterator, metadata=metadata
        )

        return recognition_stream
