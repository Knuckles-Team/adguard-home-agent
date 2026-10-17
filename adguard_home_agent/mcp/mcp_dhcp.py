"""AdGuard Home dhcp action-routed MCP tool.
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

ACTIONS = ("get_dhcp_status", "get_dhcp_interfaces", "set_dhcp_config", "find_active_dhcp", "add_dhcp_static_lease", "remove_dhcp_static_lease", "update_dhcp_static_lease", "reset_dhcp", "reset_dhcp_leases")


def register_dhcp_tools(mcp: FastMCP) -> None:
    """Register the dhcp tool."""

    @mcp.tool(tags={"dhcp"})
    async def adguard_home_dhcp(
        action: Literal["get_dhcp_status", "get_dhcp_interfaces", "set_dhcp_config", "find_active_dhcp", "add_dhcp_static_lease", "remove_dhcp_static_lease", "update_dhcp_static_lease", "reset_dhcp", "reset_dhcp_leases"] = Field(
            description="Action to perform."
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        ctx: Context | None = None,
    ) -> Any:
        """Manage adguard home dhcp operations."""
        canonical = resolve_action(action, ACTIONS, service="adguard_home_dhcp")
        if isinstance(canonical, dict):
            return canonical
        kwargs = {
            k: v for k, v in parse_json_object(params_json).items() if v is not None
        }
        return await dispatch_async(
            get_client(), canonical, kwargs, service="adguard_home_dhcp", ctx=ctx
        )
