import unittest
from unittest.mock import MagicMock

from sensory_cloud.config import Config, CloudHost
from sensory_cloud.token_manager import ITokenManager, TokenManager
from sensory_cloud.services.oauth_service import ISecureCredentialStore, OauthService
from sensory_cloud.services.assistant_service import AssistantService

import sensory_cloud.generated.v1.assistant.assistant_pb2 as assistant_pb2
import sensory_cloud.generated.v1.assistant.assistant_pb2_grpc as assistant_pb2_grpc


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


class MockAssistantService(AssistantService):
    def __init__(
        self,
        config: Config,
        token_manager: ITokenManager,
        assistant_service_client: assistant_pb2_grpc.AssistantServiceStub,
    ):
        self.config: Config = config
        self._token_manager: ITokenManager = token_manager
        self._assistant_service_client: assistant_pb2_grpc.AssistantServiceStub = (
            assistant_service_client
        )


class AssistantServiceTest(unittest.TestCase):
    cloud_host: CloudHost = CloudHost(host="domain.name")
    config: Config = Config(cloud_host=cloud_host, tenant_id="tenant-id")
    config.connect()

    credential_store: MockCredentialStore = MockCredentialStore(
        client_id="client-id", client_secret="client-secret"
    )
    oauth_service: OauthService = OauthService(
        config=config, secure_credential_store=credential_store
    )
    token_manager: TokenManager = TokenManager(oauth_service=oauth_service)
    token_manager.get_authorization_metadata = MagicMock(return_value=None)

    assistant_service_client: assistant_pb2_grpc.AssistantServiceStub = (
        assistant_pb2_grpc.AssistantServiceStub(channel=config.channel)
    )

    def test_process_message(self):
        self.config.connect()

        user_id: str = "user-id"
        device_id: str = "device-id"
        model_name: str = "my-model"
        include_audio_response: bool = False

        assistant_message_config: assistant_pb2.AssistantMessageConfig = (
            assistant_pb2.AssistantMessageConfig(
                userId=user_id,
                deviceId=device_id,
                modelName=model_name,
                includeAudioResponse=include_audio_response,
            )
        )

        mock_request: assistant_pb2.AssistantMessageRequest = (
            assistant_pb2.AssistantMessageRequest(config=assistant_message_config)
        )
        mock_response: assistant_pb2.AssistantMessageResponse = (
            assistant_pb2.AssistantMessageResponse()
        )
        self.assistant_service_client.ProcessMessage = MagicMock(
            return_value=(mock_request, mock_response)
        )

        assistant_service: MockAssistantService = MockAssistantService(
            config=self.config,
            token_manager=self.token_manager,
            assistant_service_client=self.assistant_service_client,
        )

        (
            process_message_request,
            process_message_response,
        ) = assistant_service.process_message(
            user_id=user_id,
            device_id=device_id,
            model_name=model_name,
            include_audio_response=include_audio_response,
            message_iterator=None,
        )

        self.assertIsNotNone(process_message_response)

        config_message = process_message_request.config

        self.assertEqual(
            config_message.userId, user_id, "User ID should match what was passed in"
        )
        self.assertEqual(
            config_message.deviceId,
            device_id,
            "Device ID should match what was passed in",
        )
        self.assertEqual(
            config_message.modelName,
            model_name,
            "Model name should match what was passed in",
        )
        self.assertEqual(
            config_message.includeAudioResponse,
            include_audio_response,
            "Include audio response should match what was passed in",
        )

        self.config.channel.close()


if __name__ == "__main__":
    unittest.main()
