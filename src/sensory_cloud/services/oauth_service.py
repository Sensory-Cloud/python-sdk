import grpc
import uuid
import datetime
from abc import ABC, abstractmethod

from sensory_cloud.config import Config
from sensory_cloud.services.crypto_service import CryptoService
from sensory_cloud.generated.common.common_pb2 import GenericClient
from sensory_cloud.generated.oauth.oauth_pb2_grpc import OauthServiceStub
from sensory_cloud.generated.oauth.oauth_pb2 import TokenRequest
from sensory_cloud.generated.v1.management.device_pb2_grpc import DeviceServiceStub
from sensory_cloud.generated.v1.management.device_pb2 import (
    EnrollDeviceRequest,
    DeviceResponse,
)


class OAuthClient:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
    ):
        self._client_id = client_id
        self._client_secret = client_secret

    @property
    def client_id(self) -> str:
        return self._client_id

    @property
    def client_secret(self) -> str:
        return self._client_secret


class OAuthToken:
    def __init__(self, token: str, expires: datetime.datetime):
        self._token = token
        self._expires = expires

    @property
    def token(self) -> str:
        return self._token

    @property
    def expires(self) -> str:
        return self._expires


class IOauthService(ABC):
    @abstractmethod
    def generate_credentials(self) -> OAuthClient:
        """Method that generates a client id and a client secret"""

    @abstractmethod
    def get_token(self) -> OAuthToken:
        """Method that gets a token for the provided credentials"""

    @abstractmethod
    def register(
        self, device_id: str, device_name: str, credential: str
    ) -> DeviceResponse:
        """
        Method that registers credentials provided by the attached SecureCredentialStore to Sensory Cloud.
        This should only be called once per unique credential pair.An error will be thrown if registration fails.
        """


class ISecureCredentialStore(ABC):
    @abstractmethod
    def client_id(self):
        """Method that gets the client id"""

    @abstractmethod
    def client_secret(self):
        """Method that gets the client secret"""


class OauthService(IOauthService):
    def __init__(self, config: Config, secure_credential_store: ISecureCredentialStore):
        self._config: Config = config
        self._oauth_client: OauthServiceStub = OauthServiceStub(channel=config.channel)
        self._device_client: DeviceServiceStub = DeviceServiceStub(
            channel=config.channel
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
        request: TokenRequest = TokenRequest(clientId=client_id, secret=client_secret)
        response = self._oauth_client.GetToken(request)

        return OAuthToken(
            token=response.accessToken,
            expires=now + datetime.timedelta(response.expiresIn),
        )

    def register(
        self, device_id: str, device_name: str, credential: str
    ) -> DeviceResponse:
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

        client: GenericClient = GenericClient(clientId=client_id, secret=client_secret)
        request: EnrollDeviceRequest = EnrollDeviceRequest(
            name=device_name,
            deviceId=device_id,
            tenantId=self._config.tenant_id,
            client=client,
            credential=credential,
        )
        device_response: DeviceResponse = self._device_client.EnrollDevice(request)

        return device_response
