import os
import dotenv

from sensory_cloud.config import Config
from sensory_cloud.services.oauth_service import OauthService

from secure_credential_store_example import SecureCredentialStore


dotenv.load_dotenv(override=True)


def example_device_register() -> None:

    # The device_id and device_name should be set by the user here and then stored
    # as environment variables called DEVICE_ID and DEVICE_NAME respectively for
    # use in later examples
    device_id: str = "my-new-device-id"
    device_name: str = "my-new-device-name"

    # The environment variables retrieved below should be set prior to running this example
    fully_qualified_domain_name: str = os.environ.get("FULLY_QUALIFIED_DOMAIN_NAME")
    tenant_id: str = os.environ.get("TENANT_ID")
    client_id: str = os.environ.get("CLIENT_ID")
    client_secret: str = os.environ.get("CLIENT_SECRET")
    device_credential: str = os.environ.get("DEVICE_CREDENTIAL")

    config: Config = Config(
        fully_qualified_domain_name=fully_qualified_domain_name, tenant_id=tenant_id
    )
    config.connect()

    cred_store: SecureCredentialStore = SecureCredentialStore(client_id, client_secret)

    oauth_service: OauthService = OauthService(
        config=config, secure_credential_store=cred_store
    )

    oauth_service.register(device_id, device_name, device_credential)
