"""AdGuard Home access action-routed MCP tool.
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

ACTIONS = ("get_access_list", "set_access_list")


def register_access_tools(mcp: FastMCP) -> None:
    """Register the access tool."""

    @mcp.tool(tags={"access"})
    async def adguard_home_access(
        action: Literal["get_access_list", "set_access_list"] = Field(
            description="Action to perform."
        ),
        params_json: str = Field(
            default="{}", description="JSON string of parameters to pass to the action."
        ),
        ctx: Context | None = None,
    ) -> Any:
        """Manage adguard home access operations."""
        canonical = resolve_action(action, ACTIONS, service="adguard_home_access")
        if isinstance(canonical, dict):
            return canonical
        kwargs = {
            k: v for k, v in parse_json_object(params_json).items() if v is not None
        }
        return await dispatch_async(
            get_client(), canonical, kwargs, service="adguard_home_access", ctx=ctx
        )
