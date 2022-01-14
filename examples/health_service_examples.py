import os
import dotenv

from sensory_cloud.config import Config
from sensory_cloud.generated.common.common_pb2 import ServerHealthResponse
from sensory_cloud.services.health_service import HealthService


dotenv.load_dotenv(override=True)


def health_service_example() -> ServerHealthResponse:

    # The environment variables retrieved below should be set prior to running this example
    tenant_id = os.environ.get("TENANT_ID")
    fully_qualifiied_domain_name = os.environ.get("FULLY_QUALIFIED_DOMAIN_NAME")

    config: Config = Config(
        fully_qualifiied_domain_name=fully_qualifiied_domain_name, tenant_id=tenant_id
    )
    config.connect()

    health_service: HealthService = HealthService(config=config)

    server_health: ServerHealthResponse = health_service.get_health()

    config.channel.close()

    return server_health


if __name__ == "__main__":
    server_health = health_service_example()
