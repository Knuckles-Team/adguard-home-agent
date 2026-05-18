"""Authentication module for adguard-home-agent."""

import os

from agent_utilities.base_utilities import get_logger, to_boolean

from adguard_home_agent.api_client import Api

logger = get_logger(__name__)


def get_client():
    """Get authenticated client for adguard-home-agent."""
    base_url = os.getenv("ADGUARD_BASE_URL")
    username = os.getenv("ADGUARD_USERNAME")
    password = os.getenv("ADGUARD_PASSWORD")
    verify = to_boolean(os.getenv("ADGUARD_SSL_VERIFY", "False"))
    if not base_url:
        raise RuntimeError("ADGUARD_BASE_URL not set")
    return Api(base_url=base_url, username=username, password=password, verify=verify)
