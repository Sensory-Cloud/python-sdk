import unittest
from unittest.mock import MagicMock

from sensory_cloud.config import Config
from sensory_cloud.services.health_service import HealthService
from sensory_cloud.generated.common.common_pb2 import (
    ServerHealthResponse,
    ServiceHealth,
)
from sensory_cloud.generated.health.health_pb2_grpc import HealthServiceStub


class MockHealthService(HealthService):
    def __init__(self, config: Config, health_client: HealthServiceStub):
        self._config = config
        self._health_client = health_client


class TestHealthService(unittest.TestCase):
    def test_get_health(self):
        config: Config = Config(
            fully_qualified_domain_name="domain.name", tenant_id="tenant-id"
        )
        config.connect()

        response = ServerHealthResponse(
            isHealthy=True,
            serverVersion="1.2.3",
            services=[ServiceHealth(isHealthy=True, message="ok", name="test")],
        )

        health_client = HealthServiceStub(channel=config.channel)
        health_client.GetHealth = MagicMock(return_value=response)

        health_service: MockHealthService = MockHealthService(
            config=config, health_client=health_client
        )

        health_response: ServerHealthResponse = health_service.get_health()

        self.assertEqual(health_response, response)

        config.channel.close()


if __name__ == "__main__":
    unittest.main()
