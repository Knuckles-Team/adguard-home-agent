#!/usr/bin/env python

from agent_connector_sdk.connector import Connector

from adguard_home_agent.api_client import Api
from adguard_home_agent.auth import get_client
from adguard_home_agent.mcp_server import _INSTRUCTIONS

connector = Connector(
    api=Api,
    get_client=get_client,
    instructions=_INSTRUCTIONS,
)
