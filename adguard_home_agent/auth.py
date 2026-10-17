"""Authentication and client factory for the AdGuard Home API."""

from agent_connector_sdk.config import setting

from adguard_home_agent.api_client import Api


def get_client() -> Api:
    """Return an authenticated AdGuard Home API client from the environment."""
    base_url = setting("ADGUARD_URL") or setting("ADGUARD_BASE_URL")
    if not base_url:
        raise RuntimeError("ADGUARD_URL not set")
    return Api(
        base_url=base_url,
        username=setting("ADGUARD_USERNAME"),
        password=setting("ADGUARD_PASSWORD"),
        verify=setting("ADGUARD_SSL_VERIFY", False),
    )
