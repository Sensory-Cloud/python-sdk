import unittest
from unittest.mock import MagicMock

from sensory_cloud.config import Config
from sensory_cloud.token_manager import ITokenManager, TokenManager
from sensory_cloud.services.oauth_service import ISecureCredentialStore, OauthService
from sensory_cloud.services.audio_service import AudioService
from sensory_cloud.generated.v1.audio.audio_pb2 import (
    AudioConfig,
    AudioModel,
    AuthenticateConfig,
    AuthenticateRequest,
    AuthenticateResponse,
    CreateEnrolledEventRequest,
    CreateEnrollmentConfig,
    CreateEnrollmentRequest,
    CreateEnrollmentResponse,
    GetModelsResponse,
    ThresholdSensitivity,
    TranscribeConfig,
    TranscribeRequest,
    TranscribeResponse,
    ValidateEnrolledEventConfig,
    ValidateEnrolledEventRequest,
    ValidateEnrolledEventResponse,
    ValidateEventConfig,
    ValidateEventRequest,
    ValidateEventResponse,
    CreateEnrollmentEventConfig,
)
from sensory_cloud.generated.v1.audio.audio_pb2_grpc import (
    AudioModelsStub,
    AudioBiometricsStub,
    AudioEventsStub,
    AudioTranscriptionsStub,
)


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


class MockAudioService(AudioService):
    def __init__(
        self,
        config: Config,
        token_manager: ITokenManager,
        audio_models_client: AudioModelsStub,
        audio_biometrics_client: AudioBiometricsStub,
        audio_events_client: AudioEventsStub,
        audio_transcriptions_client: AudioTranscriptionsStub,
    ):
        self.config: Config = config
        self._token_manager: ITokenManager = token_manager
        self._audio_models_client: AudioModelsStub = audio_models_client
        self._audio_biometrics_client: AudioBiometricsStub = audio_biometrics_client
        self._audio_events_client: AudioEventsStub = audio_events_client
        self._audio_transcriptions_client: AudioTranscriptionsStub = (
            audio_transcriptions_client
        )


class AudioServiceTest(unittest.TestCase):
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

    audio_models_client: AudioModelsStub = AudioModelsStub(config.channel)
    audio_biometrics_client: AudioBiometricsStub = AudioBiometricsStub(config.channel)
    audio_events_client: AudioEventsStub = AudioEventsStub(config.channel)
    audio_transcriptions_client: AudioTranscriptionsStub = AudioTranscriptionsStub(
        config.channel
    )

    audio_config: AudioConfig = AudioConfig(
        encoding=AudioConfig.AudioEncoding.Value("LINEAR16"),
        audioChannelCount=1,
        sampleRateHertz=16000,
        languageCode="en-US",
    )

    def test_get_models(self):
        self.config.connect()

        response: GetModelsResponse = GetModelsResponse(
            models=[AudioModel(name="model-name")]
        )
        self.audio_models_client.GetModels = MagicMock(return_value=response)

        audio_service: MockAudioService = MockAudioService(
            config=self.config,
            token_manager=self.token_manager,
            audio_models_client=self.audio_models_client,
            audio_biometrics_client=self.audio_biometrics_client,
            audio_events_client=self.audio_events_client,
            audio_transcriptions_client=self.audio_transcriptions_client,
        )

        models_response: GetModelsResponse = audio_service.get_models()

        self.assertEqual(models_response, response)

        self.config.channel.close()

    def test_stream_enrollment(self):
        self.config.connect()

        description: str = "my-description"
        user_id: str = "user-id"
        device_id: str = "device-id"
        model_name: str = "my-model"
        is_liveness_enabled: bool = False

        enrollment_config: CreateEnrollmentConfig = CreateEnrollmentConfig(
            audio=self.audio_config,
            description=description,
            userId=user_id,
            modelName=model_name,
            deviceId=device_id,
            isLivenessEnabled=is_liveness_enabled,
        )

        mock_request = CreateEnrollmentRequest(config=enrollment_config)
        mock_response = CreateEnrollmentResponse()
        self.audio_biometrics_client.CreateEnrollment = MagicMock(
            return_value=(mock_request, mock_response)
        )

        audio_service: MockAudioService = MockAudioService(
            config=self.config,
            token_manager=self.token_manager,
            audio_models_client=self.audio_models_client,
            audio_biometrics_client=self.audio_biometrics_client,
            audio_events_client=self.audio_events_client,
            audio_transcriptions_client=self.audio_transcriptions_client,
        )

        (
            enrollment_stream_request,
            enrollment_stream_response,
        ) = audio_service.stream_enrollment(
            audio_config=self.audio_config,
            description=description,
            user_id=user_id,
            device_id=device_id,
            model_name=model_name,
            is_liveness_enabled=is_liveness_enabled,
            audio_stream_iterator=None,
        )

        self.assertIsNotNone(enrollment_stream_response)

        config_message = enrollment_stream_request.config

        self.assertEqual(
            config_message.audio,
            self.audio_config,
            "Audio config should match what was passed in",
        )
        self.assertEqual(
            config_message.description,
            description,
            "Description should match what was passed in",
        )
        self.assertEqual(
            config_message.userId, user_id, "User ID should match what was passed in"
        )
        self.assertEqual(
            config_message.modelName,
            model_name,
            "Model name should match what was passed in",
        )
        self.assertEqual(
            config_message.isLivenessEnabled,
            is_liveness_enabled,
            "Is liveness enabled should match what was passed in",
        )

        self.config.channel.close()

    def test_stream_authentication(self):
        self.config.connect()

        enrollment_id: str = "enrollment-id"
        is_liveness_enabled: bool = False

        sensitivity: ThresholdSensitivity = ThresholdSensitivity.Value("LOW")
        security: AuthenticateConfig.ThresholdSecurity = (
            AuthenticateConfig.ThresholdSecurity.Value("LOW")
        )
        authenticate_config: AuthenticateConfig = AuthenticateConfig(
            audio=self.audio_config,
            enrollmentId=enrollment_id,
            sensitivity=sensitivity,
            security=security,
            isLivenessEnabled=is_liveness_enabled,
        )

        mock_request: AuthenticateRequest = AuthenticateRequest(
            config=authenticate_config
        )
        mock_response: AuthenticateResponse = AuthenticateResponse()
        self.audio_biometrics_client.Authenticate = MagicMock(
            return_value=(mock_request, mock_response)
        )

        audio_service: MockAudioService = MockAudioService(
            config=self.config,
            token_manager=self.token_manager,
            audio_models_client=self.audio_models_client,
            audio_biometrics_client=self.audio_biometrics_client,
            audio_events_client=self.audio_events_client,
            audio_transcriptions_client=self.audio_transcriptions_client,
        )

        (
            authenticate_stream_request,
            authenticate_stream_response,
        ) = audio_service.stream_authenticate(
            audio_config=self.audio_config,
            enrollment_id=enrollment_id,
            is_liveness_enabled=is_liveness_enabled,
            audio_stream_iterator=None,
            sensitivity=sensitivity,
            security=security,
        )

        self.assertIsNotNone(authenticate_stream_response)

        config_message = authenticate_stream_request.config

        self.assertEqual(
            config_message.audio,
            self.audio_config,
            "Audio config should match what was passed in",
        )
        self.assertEqual(
            config_message.enrollmentId,
            enrollment_id,
            "Enrollment ID should match what was passed in",
        )
        self.assertEqual(
            config_message.enrollmentGroupId, "", "Enrollment group ID should be empty"
        )
        self.assertEqual(
            config_message.sensitivity,
            sensitivity,
            "Sensitivity name should match what was passed in",
        )
        self.assertEqual(
            config_message.security,
            security,
            "Security name should match what was passed in",
        )
        self.assertEqual(
            config_message.isLivenessEnabled,
            is_liveness_enabled,
            "Is liveness enabled should match what was passed in",
        )

        self.config.channel.close()

    def test_stream_group_authentication(self):
        self.config.connect()

        enrollment_group_id: str = "enrollment-id"
        is_liveness_enabled: bool = False

        sensitivity: ThresholdSensitivity = ThresholdSensitivity.Value("LOW")
        security: AuthenticateConfig.ThresholdSecurity = (
            AuthenticateConfig.ThresholdSecurity.Value("LOW")
        )
        authenticate_config: AuthenticateConfig = AuthenticateConfig(
            audio=self.audio_config,
            enrollmentGroupId=enrollment_group_id,
            sensitivity=sensitivity,
            security=security,
            isLivenessEnabled=is_liveness_enabled,
        )

        mock_request: AuthenticateRequest = AuthenticateRequest(
            config=authenticate_config
        )
        mock_response: AuthenticateResponse = AuthenticateResponse()
        self.audio_biometrics_client.Authenticate = MagicMock(
            return_value=(mock_request, mock_response)
        )

        audio_service = MockAudioService(
            config=self.config,
            token_manager=self.token_manager,
            audio_models_client=self.audio_models_client,
            audio_biometrics_client=self.audio_biometrics_client,
            audio_events_client=self.audio_events_client,
            audio_transcriptions_client=self.audio_transcriptions_client,
        )

        (
            authenticate_stream_request,
            authenticate_stream_response,
        ) = audio_service.stream_group_authenticate(
            audio_config=self.audio_config,
            enrollment_group_id=enrollment_group_id,
            is_liveness_enabled=is_liveness_enabled,
            audio_stream_iterator=None,
            sensitivity=sensitivity,
            security=security,
        )

        self.assertIsNotNone(authenticate_stream_response)

        config_message = authenticate_stream_request.config

        self.assertEqual(
            config_message.audio,
            self.audio_config,
            "Audio config should match what was passed in",
        )
        self.assertEqual(
            config_message.enrollmentGroupId,
            enrollment_group_id,
            "Enrollment group ID should match what was passed in",
        )
        self.assertEqual(
            config_message.enrollmentId, "", "Enrollment ID should be empty"
        )
        self.assertEqual(
            config_message.sensitivity,
            sensitivity,
            "Sensitivity name should match what was passed in",
        )
        self.assertEqual(
            config_message.security,
            security,
            "Security name should match what was passed in",
        )
        self.assertEqual(
            config_message.isLivenessEnabled,
            is_liveness_enabled,
            "Is liveness enabled should match what was passed in",
        )

        self.config.channel.close()

    def test_stream_event(self):
        self.config.connect()

        model_name: str = "my-model"
        user_id: str = "user-id"
        sensitivity: ThresholdSensitivity = ThresholdSensitivity.Value("LOW")

        event_config: ValidateEventConfig = ValidateEventConfig(
            audio=self.audio_config,
            modelName=model_name,
            userId=user_id,
            sensitivity=sensitivity,
        )

        mock_request: ValidateEventRequest = ValidateEventRequest(config=event_config)
        mock_response: ValidateEventResponse = ValidateEventResponse()

        self.audio_events_client.ValidateEvent = MagicMock(
            return_value=(mock_request, mock_response)
        )

        audio_service = MockAudioService(
            config=self.config,
            token_manager=self.token_manager,
            audio_models_client=self.audio_models_client,
            audio_biometrics_client=self.audio_biometrics_client,
            audio_events_client=self.audio_events_client,
            audio_transcriptions_client=self.audio_transcriptions_client,
        )

        event_stream_request, event_stream_response = audio_service.stream_event(
            audio_config=self.audio_config,
            user_id=user_id,
            model_name=model_name,
            audio_stream_iterator=None,
            sensitivity=sensitivity,
        )

        self.assertIsNotNone(event_stream_response)

        config_message = event_stream_request.config

        self.assertEqual(
            config_message.audio,
            self.audio_config,
            "Audio config should match what was passed in",
        )
        self.assertEqual(
            config_message.userId, user_id, "User ID should match what was passed in"
        )
        self.assertEqual(
            config_message.modelName,
            model_name,
            "Model name should match what was passed in",
        )
        self.assertEqual(
            config_message.sensitivity,
            sensitivity,
            "Sensitivity name should match what was passed in",
        )

        self.config.channel.close()

    def test_stream_create_enrolled_event(self):
        self.config.connect()

        user_id: str = "user-id"
        model_name: str = "my-model"
        description: str = "my-description"

        create_enrollment_event_config: CreateEnrollmentEventConfig = (
            CreateEnrollmentEventConfig(
                audio=self.audio_config,
                userId=user_id,
                modelName=model_name,
                description=description,
            )
        )

        mock_request: CreateEnrolledEventRequest = CreateEnrolledEventRequest(
            config=create_enrollment_event_config
        )
        mock_response: CreateEnrollmentResponse = CreateEnrollmentResponse()

        self.audio_events_client.CreateEnrolledEvent = MagicMock(
            return_value=(mock_request, mock_response)
        )

        audio_service = MockAudioService(
            config=self.config,
            token_manager=self.token_manager,
            audio_models_client=self.audio_models_client,
            audio_biometrics_client=self.audio_biometrics_client,
            audio_events_client=self.audio_events_client,
            audio_transcriptions_client=self.audio_transcriptions_client,
        )

        (
            enrollment_stream_request,
            enrollment_stream_response,
        ) = audio_service.stream_create_enrolled_event(
            audio_config=self.audio_config,
            description=description,
            user_id=user_id,
            model_name=model_name,
            audio_stream_iterator=None,
        )

        self.assertIsNotNone(
            enrollment_stream_response, "Enrollment stream should be returned"
        )

        config_message = enrollment_stream_request.config

        self.assertEqual(
            config_message.audio,
            self.audio_config,
            "Audio config should match what was passed in",
        )
        self.assertEqual(
            config_message.userId, user_id, "User ID should match what was passed in"
        )
        self.assertEqual(
            config_message.modelName,
            model_name,
            "Model name should match what was passed in",
        )

        self.config.channel.close()

    def test_stream_validate_enrolled_event(self):
        self.config.connect()

        enrollment_id: str = "enrollment-id"
        sensitivity: ThresholdSensitivity = ThresholdSensitivity.Value("HIGH")

        validate_enrolled_event_config = ValidateEnrolledEventConfig(
            audio=self.audio_config,
            enrollmentId=enrollment_id,
            sensitivity=sensitivity,
        )

        mock_request: ValidateEnrolledEventRequest = ValidateEnrolledEventRequest(
            config=validate_enrolled_event_config
        )
        mock_response: ValidateEnrolledEventResponse = ValidateEnrolledEventResponse()

        self.audio_events_client.ValidateEnrolledEvent = MagicMock(
            return_value=(mock_request, mock_response)
        )

        audio_service = MockAudioService(
            config=self.config,
            token_manager=self.token_manager,
            audio_models_client=self.audio_models_client,
            audio_biometrics_client=self.audio_biometrics_client,
            audio_events_client=self.audio_events_client,
            audio_transcriptions_client=self.audio_transcriptions_client,
        )

        (
            validate_enrolled_event_request,
            validate_enrolled_event_response,
        ) = audio_service.stream_validate_enrolled_event(
            audio_config=self.audio_config,
            enrollment_id=enrollment_id,
            audio_stream_iterator=None,
            sensitivity=sensitivity,
        )

        self.assertIsNotNone(
            validate_enrolled_event_response, "Event stream should be returned"
        )

        config_message = validate_enrolled_event_request.config

        self.assertEqual(
            config_message.audio,
            self.audio_config,
            "Audio config should match what was passed in",
        )
        self.assertEqual(
            config_message.enrollmentId,
            enrollment_id,
            "Enrollment ID should match what was passed in",
        )
        self.assertEqual(
            config_message.sensitivity,
            sensitivity,
            "Sensitivity should match what was passed in",
        )

        self.config.channel.close()

    def test_stream_group_validate_enrolled_event(self):
        self.config.connect()

        enrollment_group_id: str = "enrollment-group-id"
        sensitivity: ThresholdSensitivity = ThresholdSensitivity.Value("HIGHEST")

        validate_enrolled_event_config = ValidateEnrolledEventConfig(
            audio=self.audio_config,
            enrollmentGroupId=enrollment_group_id,
            sensitivity=sensitivity,
        )

        mock_request: ValidateEnrolledEventRequest = ValidateEnrolledEventRequest(
            config=validate_enrolled_event_config
        )
        mock_response: ValidateEnrolledEventResponse = ValidateEnrolledEventResponse()

        self.audio_events_client.ValidateEnrolledEvent = MagicMock(
            return_value=(mock_request, mock_response)
        )

        audio_service = MockAudioService(
            config=self.config,
            token_manager=self.token_manager,
            audio_models_client=self.audio_models_client,
            audio_biometrics_client=self.audio_biometrics_client,
            audio_events_client=self.audio_events_client,
            audio_transcriptions_client=self.audio_transcriptions_client,
        )

        (
            validate_enrolled_event_request,
            validate_enrolled_event_response,
        ) = audio_service.stream_group_validate_enrolled_event(
            audio_config=self.audio_config,
            enrollment_group_id=enrollment_group_id,
            audio_stream_iterator=None,
            sensitivity=sensitivity,
        )

        self.assertIsNotNone(
            validate_enrolled_event_response, "Event stream should be returned"
        )

        config_message = validate_enrolled_event_request.config

        self.assertEqual(
            config_message.audio,
            self.audio_config,
            "Audio config should match what was passed in",
        )
        self.assertEqual(
            config_message.enrollmentGroupId,
            enrollment_group_id,
            "Enrollment Group ID should match what was passed in",
        )
        self.assertEqual(
            config_message.sensitivity,
            sensitivity,
            "Sensitivity should match what was passed in",
        )

        self.config.channel.close()

    def test_stream_transcription(self):
        self.config.connect()

        user_id = "user-id"
        model_name = "model-name"

        transcribe_config: TranscribeConfig = TranscribeConfig(
            audio=self.audio_config, modelName=model_name, userId=user_id
        )

        mock_request: TranscribeRequest = TranscribeRequest(config=transcribe_config)
        mock_response: TranscribeResponse = TranscribeResponse()

        self.audio_transcriptions_client.Transcribe = MagicMock(
            return_value=(mock_request, mock_response)
        )

        audio_service = MockAudioService(
            config=self.config,
            token_manager=self.token_manager,
            audio_models_client=self.audio_models_client,
            audio_biometrics_client=self.audio_biometrics_client,
            audio_events_client=self.audio_events_client,
            audio_transcriptions_client=self.audio_transcriptions_client,
        )

        (
            transcribe_stream_request,
            transcribe_stream_response,
        ) = audio_service.stream_transcription(
            audio_config=self.audio_config,
            user_id=user_id,
            model_name=model_name,
            audio_stream_iterator=None,
        )

        self.assertIsNotNone(transcribe_stream_response)

        config_message = transcribe_stream_request.config

        self.assertEqual(
            config_message.audio,
            self.audio_config,
            "Audio config should match what was passed in",
        )
        self.assertEqual(
            config_message.userId, user_id, "User ID should match what was passed in"
        )
        self.assertEqual(
            config_message.modelName,
            model_name,
            "Model name should match what was passed in",
        )

        self.config.channel.close()


if __name__ == "__main__":
    unittest.main()
