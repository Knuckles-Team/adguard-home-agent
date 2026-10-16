"""AdGuard Home rewrites action-routed MCP tool.
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

ACTIONS = ("list_rewrites", "add_rewrite", "delete_rewrite", "update_rewrite", "get_rewrite_settings", "update_rewrite_settings")


def register_rewrites_tools(mcp: FastMCP) -> None:
    """Register the rewrites tool."""

    @mcp.tool(tags={"rewrites"})
    async def adguard_home_rewrites(
        action: Literal["list_rewrites", "add_rewrite", "delete_rewrite", "update_rewrite", "get_rewrite_settings", "update_rewrite_settings"] = Field(
            description="Action to perform."
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        ctx: Context | None = None,
    ) -> Any:
        """Manage adguard home rewrites operations."""
        canonical = resolve_action(action, ACTIONS, service="adguard_home_rewrites")
        if isinstance(canonical, dict):
            return canonical
        kwargs = {
            k: v for k, v in parse_json_object(params_json).items() if v is not None
        }
        return await dispatch_async(
            get_client(), canonical, kwargs, service="adguard_home_rewrites", ctx=ctx
        )
