import unittest
import datetime

from sensory_cloud.token_manager import TokenManager, OAuthToken
from sensory_cloud.services.oauth_service import OAuthClient, IOauthService

import sensory_cloud.generated.v1.management.device_pb2 as device_pb2


class TestOauthService(IOauthService):
    def __init__(self, oauth_token: OAuthToken):
        self._oauth_token: OAuthToken = oauth_token
        self._get_token_was_called: int = 0

    @property
    def get_token_was_called(self) -> int:
        return self._get_token_was_called

    @property
    def oauth_token(self):
        return self._oauth_token

    @oauth_token.setter
    def oauth_token(self, value: OAuthToken):
        self._oauth_token = value

    def generate_credentials(self) -> OAuthClient:
        raise NotImplementedError()

    def get_token(self) -> OAuthToken:
        self._get_token_was_called += 1
        return self._oauth_token

    def register(
        self, device_id: str, device_name: str, credential: str
    ) -> device_pb2.DeviceResponse:
        raise NotImplementedError


class TokenManagerTest(unittest.TestCase):
    def test_get_token(self):
        oauth_token: OAuthToken = OAuthToken(
            token="my-token", expires=datetime.datetime.utcnow()
        )
        oauth_service: TestOauthService = TestOauthService(oauth_token=oauth_token)

        token_manager: TokenManager = TokenManager(oauth_service=oauth_service)

        token: str = token_manager.get_token()
        self.assertEqual(
            token,
            oauth_service.oauth_token.token,
            "The token returned should be correct",
        )
        self.assertEqual(
            oauth_service.get_token_was_called,
            1,
            "OAuth service should be called if no token is populated",
        )

        oauth_service.oauth_token = OAuthToken(
            token="another-token", expires=datetime.datetime.utcnow()
        )

        token: str = token_manager.get_token()
        self.assertEqual(
            token,
            oauth_service.oauth_token.token,
            "The token returned should be correct",
        )
        self.assertEqual(
            oauth_service.get_token_was_called, 2, "OAuth service should not be called"
        )

        oauth_service.oauth_token = OAuthToken(
            token="a-final-token",
            expires=datetime.datetime.utcnow() + datetime.timedelta(days=1),
        )

        token: str = token_manager.get_token()
        self.assertEqual(
            token,
            oauth_service.oauth_token.token,
            "The token returned should be correct",
        )
        self.assertEqual(
            oauth_service.get_token_was_called,
            3,
            "OAuth service should be called if token is expired",
        )

        token: str = token_manager.get_token()
        self.assertEqual(
            token,
            oauth_service.oauth_token.token,
            "The token returned should be correct",
        )
        self.assertEqual(
            oauth_service.get_token_was_called,
            3,
            "OAuth service should be called if token is expired",
        )

    def test_get_authorization_metadata(self):
        oauth_token: OAuthToken = OAuthToken(
            token="my-token", expires=datetime.datetime.utcnow()
        )
        oauth_service: TestOauthService = TestOauthService(oauth_token=oauth_token)

        token_manager: TokenManager = TokenManager(oauth_service=oauth_service)

        token_manager.get_authorization_metadata()

        self.assertEqual(
            oauth_service.get_token_was_called,
            1,
            "OAuth service should be called if no token is populated",
        )


if __name__ == "__main__":
    unittest.main()
