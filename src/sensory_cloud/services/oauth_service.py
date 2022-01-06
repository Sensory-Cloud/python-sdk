import grpc
import uuid
import datetime
from abc import ABC, abstractmethod

from sensory_cloud.config import Config
from sensory_cloud.services.crypto_service import CryptoService

import sensory_cloud.generated.common.common_pb2 as common_pb2
import sensory_cloud.generated.oauth.oauth_pb2_grpc as oauth_pb2_grpc
import sensory_cloud.generated.oauth.oauth_pb2 as oauth_pb2
import sensory_cloud.generated.v1.management.device_pb2_grpc as device_pb2_grpc
import sensory_cloud.generated.v1.management.device_pb2 as device_pb2


class OAuthClient:
    """
    Class that holds OAuth client id and secret
    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
    ):
        """
        Constructor method for the OAuthClient class

        Arguments:
            client_id: String containing the client id
            client_secret: String containing the client secret
        """

        self._client_id = client_id
        self._client_secret = client_secret

    @property
    def client_id(self) -> str:
        """
        Get method for the client id attribute

        Returns:
            String containing the client id
        """

        return self._client_id

    @property
    def client_secret(self) -> str:
        """
        Get method for the client secret attribute

        Returns:
            String containing the client secret
        """

        return self._client_secret


class OAuthToken:
    """
    Class that holds OAuth token and expiration
    """

    def __init__(self, token: str, expires: datetime.datetime):
        """
        Constructor method for the OAuthToken class

        Arguments:
            token: String containing the oauth token
            expires: datetime.datetime object containing the token's
                expiration time stamp
        """

        self._token = token
        self._expires = expires

    @property
    def token(self) -> str:
        """
        Get method that returns the oauth token attribute

        Returns:
            String containing the oauth token
        """

        return self._token

    @property
    def expires(self) -> datetime.datetime:
        """
        Get method that returns the expiration date attribute

        Returns:
            A datetime.datetime object containing the token's
                expiration time stamp
        """

        return self._expires


class IOauthService(ABC):
    """
    Abstract class that manages OAuth interactions with Sensory Cloud
    """

    @abstractmethod
    def generate_credentials(self) -> OAuthClient:
        """Method that generates a client id and a client secret"""

    @abstractmethod
    def get_token(self) -> OAuthToken:
        """Method that gets a token for the provided credentials"""

    @abstractmethod
    def register(
        self, device_id: str, device_name: str, credential: str
    ) -> device_pb2.DeviceResponse:
        """
        Method that registers credentials provided by the attached SecureCredentialStore to Sensory Cloud.
        This should only be called once per unique credential pair. An error will be thrown if registration fails.
        """


class ISecureCredentialStore(ABC):
    @abstractmethod
    def client_id(self):
        """Method that gets the client id"""

    @abstractmethod
    def client_secret(self):
        """Method that gets the client secret"""


class OauthService(IOauthService):
    """
    Class that manages OAuth interactions with Sensory Cloud
    """

    def __init__(self, config: Config, secure_credential_store: ISecureCredentialStore):
        """
        Constructor method for OauthService

        Arguments:
            config: Config object containing the relevant grpc connection information
            secure_credential_store: ISecureCredentialStore that stores the client id
                and client secret
        """

        self._config: Config = config
        self._oauth_client: oauth_pb2_grpc.OauthServiceStub = (
            oauth_pb2_grpc.OauthServiceStub(channel=config.channel)
        )
        self._device_client: device_pb2_grpc.DeviceServiceStub = (
            device_pb2_grpc.DeviceServiceStub(channel=config.channel)
        )
        self._secure_credential_store: ISecureCredentialStore = secure_credential_store

    def generate_credentials(self) -> OAuthClient:
        client = OAuthClient(
            client_id=str(uuid.uuid4()),
            client_secret=CryptoService().get_secure_random_string(length=24),
        )
        return client

    def get_token(self) -> OAuthToken:
        client_id = self._secure_credential_store.client_id
        if client_id in [None, ""]:
            raise ValueError(
                "null client_id was returned from the secure credential store"
            )

        client_secret = self._secure_credential_store.client_secret
        if client_secret in [None, ""]:
            raise ValueError(
                "null client_secret was returned from the secure credential store"
            )

        now: datetime.datetime = datetime.datetime.utcnow()
        request: oauth_pb2.TokenRequest = oauth_pb2.TokenRequest(
            clientId=client_id, secret=client_secret
        )
        response = self._oauth_client.GetToken(request)

        return OAuthToken(
            token=response.accessToken,
            expires=now + datetime.timedelta(response.expiresIn),
        )

    def register(
        self, device_id: str, device_name: str, credential: str
    ) -> device_pb2.DeviceResponse:
        client_id = self._secure_credential_store.client_id
        if client_id in [None, ""]:
            raise ValueError(
                "null client_id was returned from the secure credential store"
            )

        client_secret = self._secure_credential_store.client_secret
        if client_secret in [None, ""]:
            raise ValueError(
                "null client_secret was returned from the secure credential store"
            )

        client: common_pb2.GenericClient = common_pb2.GenericClient(
            clientId=client_id, secret=client_secret
        )
        request: device_pb2.EnrollDeviceRequest = device_pb2.EnrollDeviceRequest(
            name=device_name,
            deviceId=device_id,
            tenantId=self._config.tenant_id,
            client=client,
            credential=credential,
        )
        device_response: device_pb2.DeviceResponse = self._device_client.EnrollDevice(
            request
        )

        return device_response
