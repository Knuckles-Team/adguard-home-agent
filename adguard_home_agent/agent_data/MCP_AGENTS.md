# MCP_AGENTS.md - Dynamic Agent Registry

This file tracks the generated agents from MCP servers. You can manually modify the 'Tools' list to customize agent expertise.

## Agent Mapping Table

| Name | Description | System Prompt | Tools | Tag | Source MCP |
|------|-------------|---------------|-------|-----|------------|
| Adguard-Home Dhcp Specialist | Expert specialist for dhcp domain tasks. | You are a Adguard-Home Dhcp specialist. Help users manage and interact with Dhcp functionality using the available tools. | adguard-home-agent_dhcp_toolset | dhcp | adguard-home-agent |
| Adguard-Home Blocked Services Specialist | Expert specialist for blocked_services domain tasks. | You are a Adguard-Home Blocked Services specialist. Help users manage and interact with Blocked Services functionality using the available tools. | adguard-home-agent_blocked_services_toolset | blocked_services | adguard-home-agent |
| Adguard-Home Access Specialist | Expert specialist for access domain tasks. | You are a Adguard-Home Access specialist. Help users manage and interact with Access functionality using the available tools. | adguard-home-agent_access_toolset | access | adguard-home-agent |
| Adguard-Home System Specialist | Expert specialist for system domain tasks. | You are a Adguard-Home System specialist. Help users manage and interact with System functionality using the available tools. | adguard-home-agent_system_toolset | system | adguard-home-agent |
| Adguard-Home Settings Specialist | Expert specialist for settings domain tasks. | You are a Adguard-Home Settings specialist. Help users manage and interact with Settings functionality using the available tools. | adguard-home-agent_settings_toolset | settings | adguard-home-agent |
| Adguard-Home Rewrites Specialist | Expert specialist for rewrites domain tasks. | You are a Adguard-Home Rewrites specialist. Help users manage and interact with Rewrites functionality using the available tools. | adguard-home-agent_rewrites_toolset | rewrites | adguard-home-agent |
| Adguard-Home Filtering Specialist | Expert specialist for filtering domain tasks. | You are a Adguard-Home Filtering specialist. Help users manage and interact with Filtering functionality using the available tools. | adguard-home-agent_filtering_toolset | filtering | adguard-home-agent |
| Adguard-Home Tls Specialist | Expert specialist for tls domain tasks. | You are a Adguard-Home Tls specialist. Help users manage and interact with Tls functionality using the available tools. | adguard-home-agent_tls_toolset | tls | adguard-home-agent |
| Adguard-Home Mobile Specialist | Expert specialist for mobile domain tasks. | You are a Adguard-Home Mobile specialist. Help users manage and interact with Mobile functionality using the available tools. | adguard-home-agent_mobile_toolset | mobile | adguard-home-agent |
| Adguard-Home Stats Specialist | Expert specialist for stats domain tasks. | You are a Adguard-Home Stats specialist. Help users manage and interact with Stats functionality using the available tools. | adguard-home-agent_stats_toolset | stats | adguard-home-agent |
| Adguard-Home Clients Specialist | Expert specialist for clients domain tasks. | You are a Adguard-Home Clients specialist. Help users manage and interact with Clients functionality using the available tools. | adguard-home-agent_clients_toolset | clients | adguard-home-agent |
| Adguard-Home Dns Specialist | Expert specialist for dns domain tasks. | You are a Adguard-Home Dns specialist. Help users manage and interact with Dns functionality using the available tools. | adguard-home-agent_dns_toolset | dns | adguard-home-agent |
| Adguard-Home Profile Specialist | Expert specialist for profile domain tasks. | You are a Adguard-Home Profile specialist. Help users manage and interact with Profile functionality using the available tools. | adguard-home-agent_profile_toolset | profile | adguard-home-agent |
| Adguard-Home Query Log Specialist | Expert specialist for query_log domain tasks. | You are a Adguard-Home Query Log specialist. Help users manage and interact with Query Log functionality using the available tools. | adguard-home-agent_query_log_toolset | query_log | adguard-home-agent |
| Adguard-Home Misc Specialist | Expert specialist for misc domain tasks. | You are a Adguard-Home Misc specialist. Help users manage and interact with Misc functionality using the available tools. | adguard-home-agent_misc_toolset | misc | adguard-home-agent |

## Tool Inventory Table

| Tool Name | Description | Tag | Source |
|-----------|-------------|-----|--------|
| adguard-home-agent_dhcp_toolset | Static hint toolset for dhcp based on config env. | dhcp | adguard-home-agent |
| adguard-home-agent_blocked_services_toolset | Static hint toolset for blocked_services based on config env. | blocked_services | adguard-home-agent |
| adguard-home-agent_access_toolset | Static hint toolset for access based on config env. | access | adguard-home-agent |
| adguard-home-agent_system_toolset | Static hint toolset for system based on config env. | system | adguard-home-agent |
| adguard-home-agent_settings_toolset | Static hint toolset for settings based on config env. | settings | adguard-home-agent |
| adguard-home-agent_rewrites_toolset | Static hint toolset for rewrites based on config env. | rewrites | adguard-home-agent |
| adguard-home-agent_filtering_toolset | Static hint toolset for filtering based on config env. | filtering | adguard-home-agent |
| adguard-home-agent_tls_toolset | Static hint toolset for tls based on config env. | tls | adguard-home-agent |
| adguard-home-agent_mobile_toolset | Static hint toolset for mobile based on config env. | mobile | adguard-home-agent |
| adguard-home-agent_stats_toolset | Static hint toolset for stats based on config env. | stats | adguard-home-agent |
| adguard-home-agent_clients_toolset | Static hint toolset for clients based on config env. | clients | adguard-home-agent |
| adguard-home-agent_dns_toolset | Static hint toolset for dns based on config env. | dns | adguard-home-agent |
| adguard-home-agent_profile_toolset | Static hint toolset for profile based on config env. | profile | adguard-home-agent |
| adguard-home-agent_query_log_toolset | Static hint toolset for query_log based on config env. | query_log | adguard-home-agent |
| adguard-home-agent_misc_toolset | Static hint toolset for misc based on config env. | misc | adguard-home-agent |
