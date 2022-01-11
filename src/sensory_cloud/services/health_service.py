from sensory_cloud.config import Config

import sensory_cloud.generated.health.health_pb2_grpc as health_pb2_grpc
import sensory_cloud.generated.health.health_pb2 as health_pb2
import sensory_cloud.generated.common.common_pb2 as common_pb2


class HealthService:
    """
    Class used to obtain health status of Sensory Cloud
    """

    def __init__(self, config: Config):
        """
        Constructor method for the HealthService class

        Arguments:
            config: Config object containing the relevant grpc connection information
        """

        self._config: Config = config
        self._health_client: health_pb2_grpc.HealthServiceStub = (
            health_pb2_grpc.HealthServiceStub(channel=config.channel)
        )

    def get_health(self) -> common_pb2.ServerHealthResponse:
        """
        Method that gets the health status of the cloud endpoint defined in the Config object
        set upon construction

        Returns:
            A ServerHealthResponse object
        """

        health_request = health_pb2.HealthRequest()
        server_health_response: common_pb2.ServerHealthResponse = (
            self._health_client.GetHealth(request=health_request)
        )

        return server_health_response
