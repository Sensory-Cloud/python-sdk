import typing
from enum import Enum

from sensory_cloud.config import Config
from sensory_cloud.token_manager import ITokenManager, Metadata

import sensory_cloud.generated.v1.video.video_pb2_grpc as video_pb2_grpc
import sensory_cloud.generated.v1.video.video_pb2 as video_pb2


class VideoRequest(Enum):
    video_pb2.CreateEnrollmentRequest
    video_pb2.AuthenticateRequest
    video_pb2.ValidateRecognitionRequest


class RequestConfig(Enum):
    video_pb2.CreateEnrollmentConfig
    video_pb2.AuthenticateConfig
    video_pb2.ValidateRecognitionConfig


class RequestIterator:
    """
    The RequestIterator class facilitates the request streams that are sent to the
    grpc server.  There are three possible video request types and request configurations
    that are given by the VideoRequest and RequestConfig enums respectively.  The first
    request sent must be a configuration request and all subsequent requests contain the image
    content being streamed.
    """

    first_request: bool = True

    def __init__(
        self,
        video_request: VideoRequest,
        request_config: RequestConfig,
        video_stream_iterator: typing.Iterable[bytes],
    ):
        """
        Constructor method for the RequestIterator class

        Arguments:
            video_request: VideoRequest enum denoting which type of request is being sent
            request_config: RequestConfig enum containing the initial request configuration
            video_stream_iterator: Iterator containing image bytes
        """

        self._video_request = video_request
        self._request_config = request_config
        self._video_stream_iterator = video_stream_iterator

    def __iter__(self):
        return self

    def __next__(self):
        if self.first_request:
            self.first_request = False
            return self._video_request(config=self._request_config)
        else:
            image_content = next(self._video_stream_iterator)
            return self._video_request(imageContent=image_content)


class VideoService:
    """
    Class that handles all video requests to Sensory Cloud.
    """

    def __init__(self, config: Config, token_manager: ITokenManager):
        """
        Constructor method for the VideoService class

        Arguments:
            config: Config object containing the relevant grpc connection information
            token_manager: ITokenManager object that generates and returns JWT metadata
        """

        self._config: Config = config
        self._token_manager: ITokenManager = token_manager
        self._video_models_client: video_pb2_grpc.VideoModelsStub = (
            video_pb2_grpc.VideoModelsStub(config.channel)
        )
        self._video_biometrics_client: video_pb2_grpc.VideoBiometricsStub = (
            video_pb2_grpc.VideoBiometricsStub(config.channel)
        )
        self._video_recognition_client: video_pb2_grpc.VideoRecognitionStub = (
            video_pb2_grpc.VideoRecognitionStub(config.channel)
        )

    def get_models(self) -> video_pb2.GetModelsResponse:
        """
        Method that fetches all the video models supported by your instance of Sensory Cloud.

        Returns:
            A GetModelsResponse containing information about all video models
        """

        metadata: Metadata = self._token_manager.get_authorization_metadata()
        request: video_pb2.GetModelsRequest = video_pb2.GetModelsRequest()

        response: video_pb2.GetModelsResponse = self._video_models_client.GetModels(
            request=request, metadata=metadata
        )

        return response

    def stream_enrollment(
        self,
        description: str,
        user_id: str,
        model_name: str,
        device_id: str,
        is_liveness_enabled: bool,
        video_stream_iterator: typing.Iterable[bytes],
        threshold: video_pb2.RecognitionThreshold = video_pb2.RecognitionThreshold.Value(
            "HIGH"
        ),
        num_liveness_frames_required: int = 0,
    ) -> typing.Iterable[video_pb2.CreateEnrollmentResponse]:
        """
        Stream video to Sensory Cloud as a means for user enrollment.
        Only biometric-typed models are supported by the method.

        Arguments:
            description: String containing a description of the enrollment
            user_id: String containing the user id
            model_name: String containing the model name
            device_id: String containing the device id
            is_liveness_enabled: Boolean indicating whether or not liveness is enabled
            video_stream_iterator: Iterator of image bytes
            threshold: The liveness threshold (if liveness is enabled)
                default = RecognitionThreshold = RecognitionThreshold.Value("HIGH")
            num_liveness_frames_required: Integer indicating the number of live frames are required for a successful enrollment
                default = 0, which requires all frames to be live

        Returns:
            An iterator of CreateEnrollmentResponse objects
        """

        config: video_pb2.CreateEnrollmentConfig = video_pb2.CreateEnrollmentConfig(
            description=description,
            userId=user_id,
            deviceId=device_id,
            modelName=model_name,
            isLivenessEnabled=is_liveness_enabled,
            livenessThreshold=threshold,
            numLivenessFramesRequired=num_liveness_frames_required,
        )

        request_iterator: RequestIterator = RequestIterator(
            video_request=video_pb2.CreateEnrollmentRequest,
            request_config=config,
            video_stream_iterator=video_stream_iterator,
        )

        metadata: Metadata = self._token_manager.get_authorization_metadata()

        enrollment_stream: typing.Iterable[
            video_pb2.CreateEnrollmentResponse
        ] = self._video_biometrics_client.CreateEnrollment(
            request_iterator=request_iterator, metadata=metadata
        )

        return enrollment_stream

    def stream_authentication(
        self,
        enrollment_id: str,
        is_liveness_enabled: bool,
        video_stream_iterator: typing.Iterable[bytes],
        threshold: video_pb2.RecognitionThreshold = video_pb2.RecognitionThreshold.Value(
            "HIGH"
        ),
    ) -> typing.Iterable[video_pb2.AuthenticateResponse]:
        """
        Authenticate against an existing video enrollment in Sensory Cloud.
        Only biometric-typed models are supported by the method.

        Arguments:
            enrollment_id: String containing the enrollment id to authenticate on
            is_liveness_enabled: Boolean indicating whether or not liveness is enabled
            video_stream_iterator: Iterator of audio bytes
            threshold: The liveness threshold (if liveness is enabled)
                default = RecognitionThreshold = RecognitionThreshold.Value("HIGH")

        Returns:
            An iterator of AuthenticateResponse objects
        """

        config: video_pb2.AuthenticateConfig = video_pb2.AuthenticateConfig(
            enrollmentId=enrollment_id,
            isLivenessEnabled=is_liveness_enabled,
            livenessThreshold=threshold,
        )

        request_iterator: RequestIterator = RequestIterator(
            video_request=video_pb2.AuthenticateRequest,
            request_config=config,
            video_stream_iterator=video_stream_iterator,
        )

        metadata: Metadata = self._token_manager.get_authorization_metadata()

        authenticate_stream: typing.Iterable[
            video_pb2.AuthenticateResponse
        ] = self._video_biometrics_client.Authenticate(
            request_iterator=request_iterator, metadata=metadata
        )

        return authenticate_stream

    def stream_group_authentication(
        self,
        enrollment_group_id: str,
        is_liveness_enabled: bool,
        video_stream_iterator: typing.Iterable[bytes],
        threshold: video_pb2.RecognitionThreshold = video_pb2.RecognitionThreshold.Value(
            "HIGH"
        ),
    ) -> typing.Iterable[video_pb2.AuthenticateResponse]:
        """
        Authenticate against an existing video enrollment group in Sensory Cloud.
        Only biometric-typed models are supported by the method.

        Arguments:
            enrollment_group_id: String containing the enrollment group id to authenticate on
            is_liveness_enabled: Boolean indicating whether or not liveness is enabled
            video_stream_iterator: Iterator of audio bytes
            threshold: The liveness threshold (if liveness is enabled)
                default = RecognitionThreshold = RecognitionThreshold.Value("HIGH")

        Returns:
            An iterator of AuthenticateResponse objects
        """

        config: video_pb2.AuthenticateConfig = video_pb2.AuthenticateConfig(
            enrollmentGroupId=enrollment_group_id,
            isLivenessEnabled=is_liveness_enabled,
            livenessThreshold=threshold,
        )

        request_iterator: RequestIterator = RequestIterator(
            video_request=video_pb2.AuthenticateRequest,
            request_config=config,
            video_stream_iterator=video_stream_iterator,
        )

        metadata: Metadata = self._token_manager.get_authorization_metadata()

        authenticate_stream: typing.Iterable[
            video_pb2.AuthenticateResponse
        ] = self._video_biometrics_client.Authenticate(
            request_iterator=request_iterator, metadata=metadata
        )

        return authenticate_stream

    def stream_liveness_recognition(
        self,
        user_id: str,
        model_name: str,
        video_stream_iterator: typing.Iterable[bytes],
        threshold: video_pb2.RecognitionThreshold = video_pb2.RecognitionThreshold.Value(
            "HIGH"
        ),
    ) -> typing.Iterable[video_pb2.LivenessRecognitionResponse]:
        """
        Method that streams images to Sensory Cloud in order to recognize "liveness" of a particular image

        Arguments:
            user_id: String containing user id
            model_name: String containing the model name
            video_stream_iterator: Iterator of audio bytes
            threshold: The liveness threshold (if liveness is enabled)
                default = RecognitionThreshold = RecognitionThreshold.Value("HIGH")

        Returns:
            An iterator containing LivenessRecognitionResponse objects
        """

        config: video_pb2.ValidateRecognitionConfig = (
            video_pb2.ValidateRecognitionConfig(
                userId=user_id, modelName=model_name, threshold=threshold
            )
        )

        request_iterator: RequestIterator = RequestIterator(
            video_request=video_pb2.ValidateRecognitionRequest,
            request_config=config,
            video_stream_iterator=video_stream_iterator,
        )

        metadata: Metadata = self._token_manager.get_authorization_metadata()

        recognition_stream: typing.Iterable[
            video_pb2.LivenessRecognitionResponse
        ] = self._video_recognition_client.ValidateLiveness(
            request_iterator=request_iterator, metadata=metadata
        )

        return recognition_stream
