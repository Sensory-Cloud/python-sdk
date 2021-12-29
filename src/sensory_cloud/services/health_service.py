from sensory_cloud.config import Config
from sensory_cloud.generated.health.health_pb2_grpc import HealthServiceStub
from sensory_cloud.generated.health.health_pb2 import HealthRequest


class HealthService:
    def __init__(self, config: Config):
        self._config: Config = config
        self._health_client: HealthServiceStub = HealthServiceStub(channel=config.channel)

    def get_health(self):
        health_request = HealthRequest()
        return self._health_client.GetHealth(request=health_request)
