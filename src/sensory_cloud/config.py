import grpc
from enum import Enum


class EnrollmentType(Enum):
    none = 1
    shared_secret = 2
    jwt = 3


class SDKConfig:
    """
    All configurations required to initialize the Sensory Cloud SDK
    """

    def __init__(
        self,
        fully_qualified_domain_name: str,
        tenant_id: str,
        is_connection_secure: bool,
        enrollment_type: EnrollmentType,
        credential: str,
    ):

        self.fully_qualified_domain_name = fully_qualified_domain_name
        self.tenant_id = tenant_id
        self.is_connection_secure = is_connection_secure
        self.enrollment_type = enrollment_type
        self.credential = credential


class CloudHost:
    """
    Class for providing info on a cloud host
    """

    def __init__(
        self,
        host: str,
        port: int = 443,
        is_connection_secure: bool = True,
    ):

        host_split = host.split(":")
        if len(host_split) > 1:
            host = host_split[0]
            port = int(host_split[1])

        self.host = host
        self.port = port
        self.is_connection_secure = is_connection_secure


class Config:
    """
    Configuration class used to establish a channel with the sensory cloud server
    """

    def __init__(
        self,
        tenant_id: str,
        cloud_host: CloudHost,
    ):
        """
        Constructor method for the Config class

        Arguments:
            tenant_id: String containing the tenant to connect to
            cloud_host: CloudHost object that defines the fqdm and whether or not the
                connection is secure
        """

        self.tenant_id = tenant_id
        self.cloud_host = cloud_host
        self.fully_qualified_domain_name = f"{cloud_host.host}:{cloud_host.port}"

        self._channel = None

    def connect(self):
        """
        Public method to setup the grpc channel using the parameters that are set in the
        constructor
        """

        if self.cloud_host.is_connection_secure:
            self._channel = grpc.secure_channel(
                target=self.fully_qualified_domain_name,
                credentials=grpc.ssl_channel_credentials(),
            )
        else:
            self._channel = grpc.insecure_channel(
                target=self.fully_qualified_domain_name,
            )

    @property
    def channel(self) -> grpc.Channel:
        """
        Get method that returns the grpc channel attribute

        Returns:
            The grpc channel object set by the parameters specified in the constructor
        """

        if self._channel is None:
            raise ValueError(
                "no connection has been established with Sensory Cloud. did you forget to call connect()?"
            )
        else:
            return self._channel
