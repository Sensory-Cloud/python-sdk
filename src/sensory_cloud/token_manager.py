import datetime
import threading
import typing
from abc import ABC, abstractmethod

from sensory_cloud.services.oauth_service import IOauthService, OAuthToken


Metadata = typing.Tuple[typing.Tuple]


class ITokenManager(ABC):
    """
    Abstract class to handle the management of OAuth Tokens
    """

    @abstractmethod
    def get_token(self) -> str:
        """
        Method that gets a valid oath token

        Returns:
            A JWT as a string
        """

    @abstractmethod
    def get_authorization_metadata(self) -> Metadata:
        """
        Method that gets a token wrapped in grpc metadata

        Returns:
            A JWT wrapped in grpc metadata
        """


class TokenManager(ITokenManager):
    """
    Manages the rotation and injection of OAuth JWTs into grpc requests
    """

    _expires_buffer_seconds: int = 60 ** 2
    _token_mutex: threading.Lock = threading.Lock()
    _token: str = None
    _expires: datetime.datetime = None

    def __init__(self, oauth_service: IOauthService):
        self.oauth_service: IOauthService = oauth_service

    def get_token(self) -> str:

        self._token_mutex.acquire()

        if (
            self._token not in [None, ""]
            and self._expires is not None
            and datetime.datetime.utcnow() < self._expires
        ):
            self._token_mutex.release()
            return self._token

        try:
            oath_token = self.oauth_service.get_token()
            self._set_token(oath_token)
            self._token_mutex.release()
            return oath_token.token
        except Exception as e:
            self._token_mutex.release()
            raise (e)

    def get_authorization_metadata(self) -> Metadata:

        token: str = self.get_token()
        return (("authorization", f"Bearer {token}"),)

    def _set_token(self, oath_token: OAuthToken) -> None:
        """
        Private method that sets the _token and _expires arguments if the
        token has expired
        """

        self._token = oath_token.token
        self._expires = oath_token.expires - datetime.timedelta(
            seconds=self._expires_buffer_seconds
        )
