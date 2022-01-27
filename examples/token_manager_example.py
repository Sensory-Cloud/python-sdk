import os

from sensory_cloud.config import Config
from sensory_cloud.services.oauth_service import OAuthToken, OauthService
from sensory_cloud.token_manager import Metadata, TokenManager

from secure_credential_store_example import SecureCredentialStore


def example_token_manager():
    fully_qualifiied_domain_name: str = os.environ.get("FULLY_QUALIFIED_DOMAIN_NAME")
    tenant_id: str = os.environ.get("TENANT_ID")
    client_id: str = os.environ.get("CLIENT_ID")
    client_secret: str = os.environ.get("CLIENT_SECRET")

    config: Config = Config(
        fully_qualifiied_domain_name=fully_qualifiied_domain_name, tenant_id=tenant_id
    )
    config.connect()

    cred_store: SecureCredentialStore = SecureCredentialStore(client_id, client_secret)

    oauth_service: OauthService = OauthService(
        config=config, secure_credential_store=cred_store
    )

    token_manager: TokenManager = TokenManager(oauth_service=oauth_service)

    token: OAuthToken = token_manager.get_token()

    metadata: Metadata = token_manager.get_authorization_metadata()

    return token_manager, token, metadata


if __name__ == "__main__":
    token_manager, token, metadata = example_token_manager()
