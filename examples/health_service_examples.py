import helpers

from sensory_cloud.config import Config
from sensory_cloud.generated.common.common_pb2 import ServerHealthResponse
from sensory_cloud.services.health_service import HealthService


def health_service_example() -> ServerHealthResponse:

    config: Config = Config(
        fully_qualified_domain_name=helpers.environment_config[
            "fully_qualified_domain_name"
        ],
        tenant_id=helpers.environment_config["tenant_id"],
    )
    config.connect()

    health_service: HealthService = HealthService(config=config)

    server_health: ServerHealthResponse = health_service.get_health()

    config.channel.close()

    return server_health


if __name__ == "__main__":
    server_health = health_service_example()
