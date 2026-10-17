"""AdGuard Home settings action-routed MCP tool.
"""

from typing import Any, Literal

from agent_connector_sdk.mcp.action_dispatch import (
    dispatch_async,
    parse_json_object,
    resolve_action,
)
from fastmcp import Context, FastMCP
from pydantic import Field

from adguard_home_agent.auth import get_client

ACTIONS = ("get_parental_status", "enable_parental_control", "disable_parental_control", "get_safebrowsing_status", "enable_safebrowsing", "disable_safebrowsing", "get_safesearch_status")


def register_settings_tools(mcp: FastMCP) -> None:
    """Register the settings tool."""

    @mcp.tool(tags={"settings"})
    async def adguard_home_settings(
        action: Literal["get_parental_status", "enable_parental_control", "disable_parental_control", "get_safebrowsing_status", "enable_safebrowsing", "disable_safebrowsing", "get_safesearch_status"] = Field(
            description="Action to perform."
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        ctx: Context | None = None,
    ) -> Any:
        """Manage adguard home settings operations."""
        canonical = resolve_action(action, ACTIONS, service="adguard_home_settings")
        if isinstance(canonical, dict):
            return canonical
        kwargs = {
            k: v for k, v in parse_json_object(params_json).items() if v is not None
        }
        return await dispatch_async(
            get_client(), canonical, kwargs, service="adguard_home_settings", ctx=ctx
        )
