---
name: adguard-home-dns-management
skill_type: skill
description: >-
  Manage an AdGuard Home DNS filtering instance via the adguard-home-agent MCP
  server: inspect status and statistics, manage DNS rewrites, filtering rules,
  blocked services, clients and the query log. Use when the agent must audit or
  change DNS filtering on AdGuard Home. Do NOT use for authoritative DNS zone
  records (use dns-record-manager).
license: MIT
tags: [adguard, dns, filtering, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# AdGuard Home DNS Management

Each domain is one action-routed tool (`adguard_home_<domain>`) taking `action`
and `params_json`. Call a tool with `action="list_actions"` to discover its
actions, read before you write, and confirm before changing DNS, DHCP or
filtering configuration.

| Variable | Required | Notes |
|---|---|---|
| `ADGUARD_URL` | yes | Base URL of the AdGuard Home instance |
| `ADGUARD_USERNAME` / `ADGUARD_PASSWORD` | if auth enabled | HTTP basic credentials |
| `ADGUARD_SSL_VERIFY` | no | Verify TLS (default false) |
