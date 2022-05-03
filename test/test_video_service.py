import unittest
from unittest.mock import MagicMock

from sensory_cloud.config import Config
from sensory_cloud.generated.v1.video.video_pb2 import (
    CreateEnrollmentConfig,
    CreateEnrollmentRequest,
    CreateEnrollmentResponse,
    GetModelsResponse,
    LivenessRecognitionResponse,
    RecognitionThreshold,
    ValidateRecognitionConfig,
    ValidateRecognitionRequest,
    VideoModel,
    AuthenticateConfig,
    AuthenticateRequest,
    AuthenticateResponse,
)
from sensory_cloud.generated.v1.video.video_pb2_grpc import (
    VideoBiometricsStub,
    VideoModelsStub,
    VideoRecognitionStub,
)
from sensory_cloud.token_manager import ITokenManager, TokenManager
from sensory_cloud.services.oauth_service import ISecureCredentialStore, OauthService
from sensory_cloud.services.video_service import VideoService


class MockCredentialStore(ISecureCredentialStore):
    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret

    @property
    def client_id(self):
        return self._client_id

    @property
    def client_secret(self):
        return self._client_secret


class MockVidoService(VideoService):
    def __init__(
        self,
        config: Config,
        token_manager: ITokenManager,
        video_models_client: VideoModelsStub,
        video_biometrics_client: VideoBiometricsStub,
        video_recognition_client: VideoRecognitionStub,
    ):
        self.config: Config = config
        self._token_manager: ITokenManager = token_manager
        self._video_models_client: VideoModelsStub = video_models_client
        self._video_biometrics_client: VideoBiometricsStub = video_biometrics_client
        self._video_recognition_client: VideoRecognitionStub = video_recognition_client


class VideoServiceTest(unittest.TestCase):
    config: Config = Config(
        fully_qualified_domain_name="domain.name", tenant_id="tenant-id"
    )
    config.connect()

    credential_store: MockCredentialStore = MockCredentialStore(
        client_id="client-id", client_secret="client-secret"
    )
    oauth_service: OauthService = OauthService(
        config=config, secure_credential_store=credential_store
    )
    token_manager: TokenManager = TokenManager(oauth_service=oauth_service)
    token_manager.get_authorization_metadata = MagicMock(return_value=None)

    video_models_client: VideoModelsStub = VideoModelsStub(config.channel)
    video_biometrics_client: VideoBiometricsStub = VideoBiometricsStub(config.channel)
    video_recognition_client: VideoRecognitionStub = VideoRecognitionStub(
        config.channel
    )

    def test_get_models(self):
        self.config.connect()

        response: GetModelsResponse = GetModelsResponse(
            models=[VideoModel(name="model-name")]
        )

        self.video_models_client.GetModels = MagicMock(return_value=response)

        video_service: MockVidoService = MockVidoService(
            config=self.config,
            token_manager=self.token_manager,
            video_models_client=self.video_models_client,
            video_biometrics_client=self.video_biometrics_client,
            video_recognition_client=self.video_recognition_client,
        )

        models_response: GetModelsResponse = video_service.get_models()

        self.assertEqual(models_response, response)

        self.config.channel.close()

    def test_stream_enrollment(self):
        self.config.connect()

        description: str = "my-description"
        user_id: str = "user-id"
        model_name: str = "my-model"
        device_id: str = "my-device"
        is_liveness_enabled: bool = False
        threshold: RecognitionThreshold = RecognitionThreshold.Value("HIGH")

        enrollment_config: CreateEnrollmentConfig = CreateEnrollmentConfig(
            description=description,
            userId=user_id,
            deviceId=device_id,
            modelName=model_name,
            isLivenessEnabled=is_liveness_enabled,
            livenessThreshold=threshold,
        )

        mock_request: CreateEnrollmentRequest = CreateEnrollmentRequest(
            config=enrollment_config
        )
        mock_response: CreateEnrollmentResponse = CreateEnrollmentResponse()

        self.video_biometrics_client.CreateEnrollment = MagicMock(
            return_value=(mock_request, mock_response)
        )

        video_service: MockVidoService = MockVidoService(
            config=self.config,
            token_manager=self.token_manager,
            video_models_client=self.video_models_client,
            video_biometrics_client=self.video_biometrics_client,
            video_recognition_client=self.video_recognition_client,
        )

        (
            enrollment_stream_request,
            enrollment_stream_response,
        ) = video_service.stream_enrollment(
            description=description,
            user_id=user_id,
            model_name=model_name,
            device_id=device_id,
            is_liveness_enabled=is_liveness_enabled,
            video_stream_iterator=None,
            threshold=threshold,
        )

        self.assertIsNotNone(enrollment_stream_response)

        config_message = enrollment_stream_request.config

        self.assertEqual(config_message.description, description)
        self.assertEqual(config_message.userId, user_id)
        self.assertEqual(config_message.modelName, model_name)
        self.assertEqual(config_message.isLivenessEnabled, is_liveness_enabled)

        self.config.channel.close()

    def test_stream_authentication(self):
        self.config.connect()

        enrollment_id: str = "enrollment-id"
        is_liveness_enabled: bool = False
        threshold: RecognitionThreshold = RecognitionThreshold.Value("HIGH")

        authenticate_config: AuthenticateConfig = AuthenticateConfig(
            enrollmentId=enrollment_id,
            isLivenessEnabled=is_liveness_enabled,
            livenessThreshold=threshold,
        )

        mock_request: AuthenticateRequest = AuthenticateRequest(
            config=authenticate_config
        )
        mock_response: AuthenticateResponse = AuthenticateResponse()

        self.video_biometrics_client.Authenticate = MagicMock(
            return_value=(mock_request, mock_response)
        )

        video_service: MockVidoService = MockVidoService(
            config=self.config,
            token_manager=self.token_manager,
            video_models_client=self.video_models_client,
            video_biometrics_client=self.video_biometrics_client,
            video_recognition_client=self.video_recognition_client,
        )

        (
            authenticate_stream_request,
            authenticate_stream_response,
        ) = video_service.stream_authentication(
            enrollment_id=enrollment_id,
            is_liveness_enabled=is_liveness_enabled,
            video_stream_iterator=None,
            threshold=threshold,
        )

        self.assertIsNotNone(authenticate_stream_response)

        config_message = authenticate_stream_request.config

        self.assertEqual(config_message.enrollmentId, enrollment_id)
        self.assertEqual(config_message.livenessThreshold, threshold)
        self.assertEqual(config_message.isLivenessEnabled, is_liveness_enabled)

        self.config.channel.close()

    def test_stream_group_authentication(self):
        self.config.connect()

        enrollment_group_id: str = "enrollment-group-id"
        is_liveness_enabled: bool = False
        threshold: RecognitionThreshold = RecognitionThreshold.Value("HIGH")

        authenticate_config: AuthenticateConfig = AuthenticateConfig(
            enrollmentGroupId=enrollment_group_id,
            isLivenessEnabled=is_liveness_enabled,
            livenessThreshold=threshold,
        )

        mock_request: AuthenticateRequest = AuthenticateRequest(
            config=authenticate_config
        )
        mock_response: AuthenticateResponse = AuthenticateResponse()

        self.video_biometrics_client.Authenticate = MagicMock(
            return_value=(mock_request, mock_response)
        )

        video_service: MockVidoService = MockVidoService(
            config=self.config,
            token_manager=self.token_manager,
            video_models_client=self.video_models_client,
            video_biometrics_client=self.video_biometrics_client,
            video_recognition_client=self.video_recognition_client,
        )

        (
            authenticate_stream_request,
            authenticate_stream_response,
        ) = video_service.stream_group_authentication(
            enrollment_group_id=enrollment_group_id,
            is_liveness_enabled=is_liveness_enabled,
            video_stream_iterator=None,
            threshold=threshold,
        )

        self.assertIsNotNone(authenticate_stream_response)

        config_message = authenticate_stream_request.config

        self.assertEqual(config_message.enrollmentGroupId, enrollment_group_id)
        self.assertEqual(config_message.livenessThreshold, threshold)
        self.assertEqual(config_message.isLivenessEnabled, is_liveness_enabled)

        self.config.channel.close()

    def test_stream_recognition(self):
        self.config.connect()

        user_id: str = "user-id"
        model_name: str = "my-model"
        threshold: RecognitionThreshold = RecognitionThreshold.Value("LOW")

        recognition_config: ValidateRecognitionConfig = ValidateRecognitionConfig(
            userId=user_id, modelName=model_name, threshold=threshold
        )

        mock_request: ValidateRecognitionRequest = ValidateRecognitionRequest(
            config=recognition_config
        )
        mock_response: LivenessRecognitionResponse = LivenessRecognitionResponse()

        self.video_recognition_client.ValidateLiveness = MagicMock(
            return_value=(mock_request, mock_response)
        )

        video_service: MockVidoService = MockVidoService(
            config=self.config,
            token_manager=self.token_manager,
            video_models_client=self.video_models_client,
            video_biometrics_client=self.video_biometrics_client,
            video_recognition_client=self.video_recognition_client,
        )

        (
            liveness_recognition_request,
            liveness_recognition_response,
        ) = video_service.stream_liveness_recognition(
            user_id=user_id,
            model_name=model_name,
            video_stream_iterator=None,
            threshold=threshold,
        )

        self.assertIsNotNone(liveness_recognition_response)

        config_message = liveness_recognition_request.config

        self.assertEqual(config_message.userId, user_id)
        self.assertEqual(config_message.threshold, threshold)
        self.assertEqual(config_message.modelName, model_name)

        self.config.channel.close()
