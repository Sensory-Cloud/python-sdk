from sensory_cloud.config import Config
from sensory_cloud.generated.health.health_pb2_grpc import HealthServiceStub
from sensory_cloud.generated.health.health_pb2 import HealthRequest
from sensory_cloud.generated.common.common_pb2 import ServerHealthResponse


class HealthService:
    def __init__(self, config: Config):
        
        self._config: Config = config
        self._health_client: HealthServiceStub = HealthServiceStub(channel=config.channel)

    def get_health(self) -> ServerHealthResponse:
        
        health_request = HealthRequest()
        server_health_response: ServerHealthResponse = self._health_client.GetHealth(request=health_request)

        return server_health_response
