"""AdGuard Home blocked-services action-routed MCP tool.
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

ACTIONS = ("get_blocked_services_list", "get_all_blocked_services", "update_blocked_services")


def register_blocked_services_tools(mcp: FastMCP) -> None:
    """Register the blocked-services tool."""

    @mcp.tool(tags={"blocked-services"})
    async def adguard_home_blocked_services(
        action: Literal["get_blocked_services_list", "get_all_blocked_services", "update_blocked_services"] = Field(
            description="Action to perform."
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        ctx: Context | None = None,
    ) -> Any:
        """Manage adguard home blocked services operations."""
        canonical = resolve_action(action, ACTIONS, service="adguard_home_blocked_services")
        if isinstance(canonical, dict):
            return canonical
        kwargs = {
            k: v for k, v in parse_json_object(params_json).items() if v is not None
        }
        return await dispatch_async(
            get_client(), canonical, kwargs, service="adguard_home_blocked_services", ctx=ctx
        )
