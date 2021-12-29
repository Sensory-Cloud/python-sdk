import grpc


class Config:
    def __init__(
        self, 
        fully_qualifiied_domain_name: str,
        tenant_id: str,
        is_connection_secure: bool = True,
    ):
        self.fully_qualifiied_domain_name = fully_qualifiied_domain_name
        self.is_connection_secure = is_connection_secure
        self.tenant_id = tenant_id

        self._channel = None

    def connect(self):
        if self.is_connection_secure:
            self._channel = grpc.secure_channel(
                target=self.fully_qualifiied_domain_name, 
                credentials=grpc.ssl_channel_credentials()
            )
        else:
            self._channel = grpc.insecure_channel(
                target=self.fully_qualifiied_domain_name,
            )

    @property
    def channel(self):
        if self._channel is None:
            raise ValueError("no connection has been established with Sensory Cloud. did you forget to call connect()?")
        else:
            return self._channel

