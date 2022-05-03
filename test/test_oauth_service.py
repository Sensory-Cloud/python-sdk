import datetime
import re
import unittest
from unittest.mock import MagicMock

from sensory_cloud.config import Config
from sensory_cloud.services.oauth_service import (
    IOauthService,
    ISecureCredentialStore,
    OAuthToken,
    OauthService,
)

import sensory_cloud.generated.common.common_pb2 as common_pb2
import sensory_cloud.generated.v1.management.device_pb2 as device_pb2
import sensory_cloud.generated.v1.management.device_pb2_grpc as device_pb2_grpc
import sensory_cloud.generated.oauth.oauth_pb2_grpc as oauth_pb2_grpc


def is_valid_guuid(str):

    # Regex to check valid
    # GUID (Globally Unique Identifier)
    regex = "^[{]?[0-9a-fA-F]{8}" + "-([0-9a-fA-F]{4}-)" + "{3}[0-9a-fA-F]{12}[}]?$"

    # Compile the ReGex
    p = re.compile(regex)

    # If the string is empty
    # return false
    if str == None:
        return False

    # Return if the string
    # matched the ReGex
    if re.search(p, str):
        return True
    else:
        return False


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


class MockOAuthService(OauthService):
    def __init__(
        self,
        config: Config,
        secure_credential_store: ISecureCredentialStore,
        oauth_client: oauth_pb2_grpc.OauthServiceStub,
        device_client: device_pb2_grpc.DeviceServiceStub,
    ):

        self._config: Config = config
        self._oauth_client: oauth_pb2_grpc.OauthServiceStub = oauth_client
        self._device_client: device_pb2_grpc.DeviceServiceStub = device_client
        self._secure_credential_store: ISecureCredentialStore = secure_credential_store


class OauthServiceTest(unittest.TestCase):
    config: Config = Config(
        fully_qualified_domain_name="domain.name", tenant_id="tenant-id"
    )
    config.connect()

    oauth_client: oauth_pb2_grpc.OauthServiceStub = oauth_pb2_grpc.OauthServiceStub(
        config.channel
    )
    device_client: device_pb2_grpc.DeviceServiceStub = (
        device_pb2_grpc.DeviceServiceStub(config.channel)
    )

    def test_generate_credentials(self):
        self.config.connect()

        credential_store: MockCredentialStore = MockCredentialStore(
            client_id="client-id", client_secret="client-secret"
        )

        oauth_service: MockOAuthService = MockOAuthService(
            config=self.config,
            secure_credential_store=credential_store,
            oauth_client=self.oauth_client,
            device_client=self.device_client,
        )

        credentials = oauth_service.generate_credentials()

        self.assertTrue(
            is_valid_guuid(credentials.client_id),
            "The generated clientId should be a valid GUID",
        )
        self.assertEqual(
            len(credentials.client_secret),
            24,
            "The generated secret should be exactly 24 characters",
        )

        self.config.channel.close()

    def test_get_who_am_i(self):
        self.config.connect()

        credential_store: MockCredentialStore = MockCredentialStore(
            client_id="client-id", client_secret="client-secret"
        )

        mock_token_response: common_pb2.TokenResponse = common_pb2.TokenResponse(
            accessToken="my-token", expiresIn=0
        )
        self.oauth_client.GetToken = MagicMock(return_value=mock_token_response)

        mock_device_response: device_pb2.DeviceResponse = device_pb2.DeviceResponse(
            name="my-device-name", deviceId="my-device-id"
        )
        self.device_client.GetWhoAmI = MagicMock(return_value=mock_device_response)

        oauth_service: MockOAuthService = MockOAuthService(
            config=self.config,
            secure_credential_store=credential_store,
            oauth_client=self.oauth_client,
            device_client=self.device_client,
        )

        device_response: device_pb2.DeviceResponse = oauth_service.get_who_am_i()

        self.assertEqual(
            device_response,
            mock_device_response,
            "the who am I response should be correct",
        )

        self.config.channel.close()

    def test_get_token_null_credentials(self):
        self.config.connect()

        null_id_credential_store: MockCredentialStore = MockCredentialStore(
            client_id=None, client_secret="client-secret"
        )

        oauth_service: OauthService = OauthService(
            config=self.config, secure_credential_store=null_id_credential_store
        )

        self.assertRaises(ValueError, oauth_service.get_token)

        null_secret_credential_store: MockCredentialStore = MockCredentialStore(
            client_id="client-id", client_secret=""
        )
        oauth_service: OauthService = OauthService(
            config=self.config, secure_credential_store=null_secret_credential_store
        )

        self.assertRaises(ValueError, oauth_service.get_token)

        self.config.channel.close()

    def test_get_token(self):
        self.config.connect()

        credential_store: MockCredentialStore = MockCredentialStore(
            client_id="client-id", client_secret="client-secret"
        )

        token_response: common_pb2.TokenResponse = common_pb2.TokenResponse(
            accessToken="fake-token", expiresIn=0
        )
        self.oauth_client.GetToken = self.oauth_client.GetToken = MagicMock(
            return_value=token_response
        )

        oauth_service: MockOAuthService = MockOAuthService(
            config=self.config,
            secure_credential_store=credential_store,
            oauth_client=self.oauth_client,
            device_client=self.device_client,
        )

        oauth_token: OAuthToken = oauth_service.get_token()

        self.assertEqual(
            oauth_token.token,
            token_response.accessToken,
            "Returned access token should be the same",
        )
        self.assertTrue(
            oauth_token.expires <= datetime.datetime.utcnow(),
            "Token expiration should be earlier than or equal to now",
        )

        self.config.channel.close()

    def test_register_null_credentials(self):
        self.config.connect()

        device_name = "device-name"
        device_id = "device-id"
        credential = "credential"

        null_id_credential_store: MockCredentialStore = MockCredentialStore(
            client_id=None, client_secret="client-secret"
        )
        oauth_service: OauthService = OauthService(
            config=self.config, secure_credential_store=null_id_credential_store
        )
        self.assertRaises(
            ValueError, oauth_service.register, device_id, device_name, credential
        )

        null_secret_credential_store: MockCredentialStore = MockCredentialStore(
            client_id="client-id", client_secret=""
        )
        oauth_service: OauthService = OauthService(
            config=self.config, secure_credential_store=null_secret_credential_store
        )
        self.assertRaises(
            ValueError, oauth_service.register, device_id, device_name, credential
        )

        self.config.channel.close()

    def test_register(self):
        self.config.connect()

        device_name: str = "device-name"
        device_id: str = "device-id"
        credential: str = "my-credential"

        credential_store: MockCredentialStore = MockCredentialStore(
            client_id="client-id", client_secret="client-secret"
        )

        response: device_pb2.DeviceResponse = device_pb2.DeviceResponse(
            name=device_name, deviceId=device_id
        )
        self.device_client.EnrollDevice = MagicMock(return_value=response)

        oauth_service: MockOAuthService = MockOAuthService(
            config=self.config,
            secure_credential_store=credential_store,
            oauth_client=self.oauth_client,
            device_client=self.device_client,
        )

        device_response: device_pb2.DeviceResponse = oauth_service.register(
            device_id=device_id, device_name=device_name, credential=credential
        )

        self.assertEqual(
            response.name,
            device_response.name,
            "Returned device name should be the same",
        )
        self.assertEqual(
            response.deviceId,
            device_response.deviceId,
            "Returned device id should be the same",
        )

        self.config.channel.close()

    def test_renew_device_credential(self):
        self.config.connect()

        device_id: str = "device-id"
        credential: str = "my-credential"

        credential_store: MockCredentialStore = MockCredentialStore(
            client_id="client-id", client_secret="client-secret"
        )

        mock_token_response: common_pb2.TokenResponse = common_pb2.TokenResponse(
            accessToken="my-token", expiresIn=0
        )
        self.oauth_client.GetToken = MagicMock(return_value=mock_token_response)

        mock_device_response: device_pb2.DeviceResponse = device_pb2.DeviceResponse(
            name="my-device-name", deviceId=device_id
        )
        self.device_client.RenewDeviceCredential = MagicMock(return_value=mock_device_response)

        oauth_service: MockOAuthService = MockOAuthService(
            config=self.config,
            secure_credential_store=credential_store,
            oauth_client=self.oauth_client,
            device_client=self.device_client,
        )

        device_response: device_pb2.DeviceResponse = oauth_service.renew_device_credential(device_id=device_id, credential=credential)

        self.assertEqual(
            device_response,
            mock_device_response,
            "the who am I response should be correct",
        )

        self.config.channel.close()

if __name__ == "__main__":
    unittest.main()
