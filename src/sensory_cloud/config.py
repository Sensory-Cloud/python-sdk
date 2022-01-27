import grpc


class Config:
    """
    Configuration class used to establish a channel with the sensory cloud server
    """

    def __init__(
        self,
        fully_qualified_domain_name: str,
        tenant_id: str,
        is_connection_secure: bool = True,
    ):
        """
        Constructor method for the Config class

        Arguments:
            fully_qualified_domain_name: String containing the domain to connect to
            tenant_id: String containing the tenant to connect to
            is_connection_secure: Boolean denoting whether or not to establish a secure
                grpc connection
        """

        self.fully_qualified_domain_name = fully_qualified_domain_name
        self.is_connection_secure = is_connection_secure
        self.tenant_id = tenant_id

        self._channel = None

    def connect(self):
        """
        Public method to setup the grpc channel using the parameters that are set in the
        constructor
        """

        if self.is_connection_secure:
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
