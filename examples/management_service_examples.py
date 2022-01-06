import os
import dotenv

from sensory_cloud.services.management_service import ManagementService
from sensory_cloud.config import Config
from sensory_cloud.token_manager import TokenManager
from sensory_cloud.services.oauth_service import OauthService

from secure_credential_store_example import SecureCredentialStore

dotenv.load_dotenv(override=True)


def example_management_service() -> ManagementService:

    fully_qualifiied_domain_name = os.environ.get("FULLY_QUALIFIED_DOMAIN_NAME")
    tenant_id = os.environ.get("TENANT_ID")
    client_id = os.environ.get("CLIENT_ID")
    client_secret = os.environ.get("CLIENT_SECRET")

    config = Config(
        fully_qualifiied_domain_name=fully_qualifiied_domain_name, tenant_id=tenant_id
    )
    config.connect()

    cred_store = SecureCredentialStore(client_id, client_secret)
    oauth_service = OauthService(config=config, secure_credential_store=cred_store)

    token_manager = TokenManager(oauth_service=oauth_service)

    management_service = ManagementService(config=config, token_manager=token_manager)

    return management_service
