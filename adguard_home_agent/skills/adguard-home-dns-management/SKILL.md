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

Each API operation is its own typed tool (`adguard_home_<operation>`). Read
before you write, and confirm before changing DNS, DHCP or
filtering configuration.

| Variable | Required | Notes |
|---|---|---|
| `ADGUARD_URL` | yes | Base URL of the AdGuard Home instance |
| `ADGUARD_USERNAME` / `ADGUARD_PASSWORD` | if auth enabled | HTTP basic credentials |
| `ADGUARD_SSL_VERIFY` | no | Verify TLS (default false) |
