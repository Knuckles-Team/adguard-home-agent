"""AdGuard Home graph configuration — tag prompts and env var mappings.

This is the only file needed to enable graph mode for this agent.
Provides TAG_PROMPTS and TAG_ENV_VARS for create_graph_agent_server().
"""

TAG_PROMPTS: dict[str, str] = {
    "access": (
        "You are a AdGuard Home Access specialist. Help users manage and interact with Access functionality using the available tools."
    ),
    "blocked-services": (
        "You are a AdGuard Home Blocked Services specialist. Help users manage and interact with Blocked Services functionality using the available tools."
    ),
    "clients": (
        "You are a AdGuard Home Clients specialist. Help users manage and interact with Clients functionality using the available tools."
    ),
    "dhcp": (
        "You are a AdGuard Home Dhcp specialist. Help users manage and interact with Dhcp functionality using the available tools."
    ),
    "dns": (
        "You are a AdGuard Home Dns specialist. Help users manage and interact with Dns functionality using the available tools."
    ),
    "filtering": (
        "You are a AdGuard Home Filtering specialist. Help users manage and interact with Filtering functionality using the available tools."
    ),
    "mobile": (
        "You are a AdGuard Home Mobile specialist. Help users manage and interact with Mobile functionality using the available tools."
    ),
    "profile": (
        "You are a AdGuard Home Profile specialist. Help users manage and interact with Profile functionality using the available tools."
    ),
    "query-log": (
        "You are a AdGuard Home Query Log specialist. Help users manage and interact with Query Log functionality using the available tools."
    ),
    "rewrites": (
        "You are a AdGuard Home Rewrites specialist. Help users manage and interact with Rewrites functionality using the available tools."
    ),
    "settings": (
        "You are a AdGuard Home Settings specialist. Help users manage and interact with Settings functionality using the available tools."
    ),
    "stats": (
        "You are a AdGuard Home Stats specialist. Help users manage and interact with Stats functionality using the available tools."
    ),
    "system": (
        "You are a AdGuard Home System specialist. Help users manage and interact with System functionality using the available tools."
    ),
    "tls": (
        "You are a AdGuard Home Tls specialist. Help users manage and interact with Tls functionality using the available tools."
    ),
}


TAG_ENV_VARS: dict[str, str] = {
    "access": "ACCESSTOOL",
    "blocked-services": "BLOCKED_SERVICESTOOL",
    "clients": "CLIENTSTOOL",
    "dhcp": "DHCPTOOL",
    "dns": "DNSTOOL",
    "filtering": "FILTERINGTOOL",
    "mobile": "MOBILETOOL",
    "profile": "PROFILETOOL",
    "query-log": "QUERY_LOGTOOL",
    "rewrites": "REWRITESTOOL",
    "settings": "SETTINGSTOOL",
    "stats": "STATSTOOL",
    "system": "SYSTEMTOOL",
    "tls": "TLSTOOL",
}
