# Configuration

| Variable | Default | Notes |
|---|---|---|
| `ADGUARD_URL` | required | Base URL of the AdGuard Home instance (`ADGUARD_BASE_URL` is accepted as a legacy alias) |
| `ADGUARD_USERNAME` / `ADGUARD_PASSWORD` | unset | HTTP basic credentials |
| `ADGUARD_TLS_PROFILE` / `ADGUARD_CA_BUNDLE_REF` | unset | Runtime TLS profile (SDK `resolve_tls_profile`); verification is always on, so supply a CA bundle for a private CA |
| `<DOMAIN>TOOL` | `True` | Enable one tool suite, for example `DNSTOOL`, `QUERY_LOGTOOL` |
| `MCP_TOOL_MODE` | `condensed` | Tool surface mode |
| `TRANSPORT` / `HOST` / `PORT` | `stdio` / `0.0.0.0` / `8000` | MCP transport |
