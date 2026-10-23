# Configuration

| Variable | Default | Notes |
|---|---|---|
| `ADGUARD_URL` | required | Base URL of the AdGuard Home instance (`ADGUARD_BASE_URL` is accepted as a legacy alias) |
| `ADGUARD_USERNAME` / `ADGUARD_PASSWORD` | unset | HTTP basic credentials |
| `ADGUARD_CA_BUNDLE` / `ADGUARD_CA_BUNDLE_REF` / `ADGUARD_TLS_PROFILE` | unset | Extra CA for a private-CA instance, via the shared TLS profile; verification is always on and cannot be disabled |
| `<DOMAIN>TOOL` | `True` | Enable one tool suite, for example `DNSTOOL`, `QUERY_LOGTOOL` |
| `MCP_TOOL_MODE` | `condensed` | Tool surface mode |
| `TRANSPORT` / `HOST` / `PORT` | `stdio` / `0.0.0.0` / `8000` | MCP transport |
