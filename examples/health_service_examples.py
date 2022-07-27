import helpers

from sensory_cloud.config import Config, CloudHost
from sensory_cloud.generated.common.common_pb2 import ServerHealthResponse
from sensory_cloud.services.health_service import HealthService


def health_service_example() -> ServerHealthResponse:

    cloud_host: CloudHost = CloudHost(
        host=helpers.environment_config.get(
            "SDK-configuration", "fullyQualifiedDomainName"
        ),
        is_connection_secure=helpers.environment_config.getboolean(
            "SDK-configuration", "isSecure"
        ),
    )
    config: Config = Config(
        cloud_host=cloud_host,
        tenant_id=helpers.environment_config.get("SDK-configuration", "tenantId"),
    )
    config.connect()

    health_service: HealthService = HealthService(config=config)

    server_health: ServerHealthResponse = health_service.get_health()

    config.channel.close()

    return server_health


if __name__ == "__main__":
    server_health: ServerHealthResponse = health_service_example()
