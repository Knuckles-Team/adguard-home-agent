"""MCP tool registration modules — one action-routed module per domain tag.

"""

from adguard_home_agent.mcp.mcp_system import register_system_tools
from adguard_home_agent.mcp.mcp_access import register_access_tools
from adguard_home_agent.mcp.mcp_blocked_services import register_blocked_services_tools
from adguard_home_agent.mcp.mcp_filtering import register_filtering_tools
from adguard_home_agent.mcp.mcp_clients import register_clients_tools
from adguard_home_agent.mcp.mcp_profile import register_profile_tools
from adguard_home_agent.mcp.mcp_dhcp import register_dhcp_tools
from adguard_home_agent.mcp.mcp_settings import register_settings_tools
from adguard_home_agent.mcp.mcp_query_log import register_query_log_tools
from adguard_home_agent.mcp.mcp_rewrites import register_rewrites_tools
from adguard_home_agent.mcp.mcp_tls import register_tls_tools
from adguard_home_agent.mcp.mcp_mobile import register_mobile_tools
from adguard_home_agent.mcp.mcp_stats import register_stats_tools
from adguard_home_agent.mcp.mcp_dns import register_dns_tools

__all__ = [
    "register_system_tools",
    "register_access_tools",
    "register_blocked_services_tools",
    "register_filtering_tools",
    "register_clients_tools",
    "register_profile_tools",
    "register_dhcp_tools",
    "register_settings_tools",
    "register_query_log_tools",
    "register_rewrites_tools",
    "register_tls_tools",
    "register_mobile_tools",
    "register_stats_tools",
    "register_dns_tools",
]
