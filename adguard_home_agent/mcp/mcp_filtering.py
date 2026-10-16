"""AdGuard Home filtering action-routed MCP tool.
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

ACTIONS = ("set_filtering_rules", "check_host_filtering", "set_filter_url_params", "get_filtering_status", "set_filtering_config", "add_filter_url", "remove_filter_url", "refresh_filters")


def register_filtering_tools(mcp: FastMCP) -> None:
    """Register the filtering tool."""

    @mcp.tool(tags={"filtering"})
    async def adguard_home_filtering(
        action: Literal["set_filtering_rules", "check_host_filtering", "set_filter_url_params", "get_filtering_status", "set_filtering_config", "add_filter_url", "remove_filter_url", "refresh_filters"] = Field(
            description="Action to perform."
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        ctx: Context | None = None,
    ) -> Any:
        """Manage adguard home filtering operations."""
        canonical = resolve_action(action, ACTIONS, service="adguard_home_filtering")
        if isinstance(canonical, dict):
            return canonical
        kwargs = {
            k: v for k, v in parse_json_object(params_json).items() if v is not None
        }
        return await dispatch_async(
            get_client(), canonical, kwargs, service="adguard_home_filtering", ctx=ctx
        )
