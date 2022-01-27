<<<<<<< HEAD
import helpers
=======
import os
import dotenv
>>>>>>> main

from sensory_cloud.config import Config
from sensory_cloud.generated.common.common_pb2 import ServerHealthResponse
from sensory_cloud.services.health_service import HealthService


<<<<<<< HEAD
def health_service_example() -> ServerHealthResponse:

    config: Config = Config(
        fully_qualified_domain_name=helpers.environment_config["fully_qualified_domain_name"], 
        tenant_id=helpers.environment_config["tenant_id"]
=======
dotenv.load_dotenv(override=True)


tenant_id = os.environ.get("TENANT_ID")
device_id = os.environ.get("DEVICE_ID")
fully_qualifiied_domain_name = os.environ.get("FULLY_QUALIFIED_DOMAIN_NAME")


def health_service_example() -> ServerHealthResponse:

    config: Config = Config(
        fully_qualifiied_domain_name=fully_qualifiied_domain_name, tenant_id=tenant_id
>>>>>>> main
    )
    config.connect()

    health_service: HealthService = HealthService(config=config)

    server_health: ServerHealthResponse = health_service.get_health()

    config.channel.close()

    return server_health


if __name__ == "__main__":
    server_health = health_service_example()
