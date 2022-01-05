import re
import unittest
from unittest.mock import MagicMock

from sensory_cloud.config import Config
from sensory_cloud.generated.common.common_pb2 import TokenResponse
from sensory_cloud.generated.v1.management.device_pb2 import DeviceResponse
from sensory_cloud.services.oauth_service import (
    ISecureCredentialStore,
    OAuthToken,
    OauthService,
)


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


class OauthServiceTest(unittest.TestCase):
    def test_generate_credentials(self):
        credential_store: MockCredentialStore = MockCredentialStore(
            client_id="client-id", client_secret="client-secret"
        )
        config: Config = Config(
            fully_qualifiied_domain_name="domain.name", tenant_id="tenant-id"
        )
        config.connect()

        oauth_service: OauthService = OauthService(
            config=config, secure_credential_store=credential_store
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

        config.channel.close()

    def test_get_token_null_credentials(self):
        null_id_credential_store: MockCredentialStore = MockCredentialStore(
            client_id=None, client_secret="client-secret"
        )
        config: Config = Config(
            fully_qualifiied_domain_name="domain.name", tenant_id="tenant-id"
        )
        config.connect()

        oauth_service: OauthService = OauthService(
            config=config, secure_credential_store=null_id_credential_store
        )

        self.assertRaises(ValueError, oauth_service.get_token)

        null_secret_credential_store: MockCredentialStore = MockCredentialStore(
            client_id="client-id", client_secret=""
        )
        oauth_service: OauthService = OauthService(
            config=config, secure_credential_store=null_secret_credential_store
        )

        self.assertRaises(ValueError, oauth_service.get_token)

        config.channel.close()

    def test_get_token(self):
        credential_store: MockCredentialStore = MockCredentialStore(
            client_id="client-id", client_secret="client-secret"
        )
        config: Config = Config(
            fully_qualifiied_domain_name="domain.name", tenant_id="tenant-id"
        )
        config.connect()

        oauth_service: OauthService = OauthService(
            config=config, secure_credential_store=credential_store
        )

        token_response: TokenResponse = TokenResponse(
            accessToken="fake-token", expiresIn=0
        )

        oauth_service.get_token = MagicMock(
            return_value=OAuthToken(
                token=token_response.accessToken, expires=token_response.expiresIn
            )
        )
        oauth_token: OAuthToken = oauth_service.get_token()

        self.assertEqual(
            oauth_token.token,
            token_response.accessToken,
            "Returned access token should be the same",
        )
        self.assertTrue(
            oauth_token.expires <= 0,
            "Token expiration should be earlier than or equal to now",
        )

        config.channel.close()

    def test_register_null_credentials(self):
        device_name = "device-name"
        device_id = "device-id"
        credential = "credential"

        config: Config = Config(
            fully_qualifiied_domain_name="domain.name", tenant_id="tenant-id"
        )
        config.connect()

        null_id_credential_store: MockCredentialStore = MockCredentialStore(
            client_id=None, client_secret="client-secret"
        )
        oauth_service: OauthService = OauthService(
            config=config, secure_credential_store=null_id_credential_store
        )
        self.assertRaises(
            ValueError, oauth_service.register, device_id, device_name, credential
        )

        null_secret_credential_store: MockCredentialStore = MockCredentialStore(
            client_id="client-id", client_secret=""
        )
        oauth_service: OauthService = OauthService(
            config=config, secure_credential_store=null_secret_credential_store
        )
        self.assertRaises(
            ValueError, oauth_service.register, device_id, device_name, credential
        )

        config.channel.close()

    def test_register(self):
        device_name = "device-name"
        device_id = "device-id"

        config: Config = Config(
            fully_qualifiied_domain_name="domain.name", tenant_id="tenant-id"
        )
        config.connect()

        credential_store: MockCredentialStore = MockCredentialStore(
            client_id="client-id", client_secret="client-secret"
        )

        response: DeviceResponse = DeviceResponse(name=device_name, deviceId=device_id)

        oauth_service: OauthService = OauthService(
            config=config, secure_credential_store=credential_store
        )
        oauth_service.register = MagicMock(return_value=response)

        device_response = oauth_service.register()

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

    def test_dummy(self):
        self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
