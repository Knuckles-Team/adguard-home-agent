#!/usr/bin/env python
# coding: utf-8

import sys
import json
import os
import argparse
import logging
import uvicorn
import httpx
from typing import Optional, Any
from contextlib import asynccontextmanager
from pydantic_ai import Agent, ModelSettings, RunContext
from pydantic_ai.mcp import (
    load_mcp_servers,
    MCPServerStreamableHTTP,
    MCPServerSSE,
)
from pydantic_ai_skills import SkillsToolset
from fasta2a import Skill
from adguard_home_agent.utils import (
    to_integer,
    to_boolean,
    to_float,
    to_list,
    to_dict,
    get_mcp_config_path,
    get_skills_path,
    load_skills_from_directory,
    create_model,
    tool_in_tag,
    prune_large_messages,
)

from fastapi import FastAPI, Request
from starlette.responses import Response, StreamingResponse
from pydantic import ValidationError
from pydantic_ai.ui import SSE_CONTENT_TYPE
from pydantic_ai.ui.ag_ui import AGUIAdapter

__version__ = "0.2.11"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logging.getLogger("pydantic_ai").setLevel(logging.INFO)
logging.getLogger("fastmcp").setLevel(logging.INFO)
logging.getLogger("httpx").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_HOST = os.getenv("HOST", "0.0.0.0")
DEFAULT_PORT = to_integer(string=os.getenv("PORT", "9000"))
DEFAULT_DEBUG = to_boolean(string=os.getenv("DEBUG", "False"))
DEFAULT_PROVIDER = os.getenv("PROVIDER", "openai")
DEFAULT_MODEL_ID = os.getenv("MODEL_ID", "qwen/qwen3-coder-next")
DEFAULT_LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://host.docker.internal:1234/v1")
DEFAULT_LLM_API_KEY = os.getenv("LLM_API_KEY", "ollama")
DEFAULT_MCP_URL = os.getenv("MCP_URL", None)
DEFAULT_MCP_CONFIG = os.getenv("MCP_CONFIG", get_mcp_config_path())
DEFAULT_CUSTOM_SKILLS_DIRECTORY = os.getenv("CUSTOM_SKILLS_DIRECTORY", None)
DEFAULT_ENABLE_WEB_UI = to_boolean(os.getenv("ENABLE_WEB_UI", "False"))
DEFAULT_SSL_VERIFY = to_boolean(os.getenv("SSL_VERIFY", "True"))

DEFAULT_MAX_TOKENS = to_integer(os.getenv("MAX_TOKENS", "16384"))
DEFAULT_TEMPERATURE = to_float(os.getenv("TEMPERATURE", "0.7"))
DEFAULT_TOP_P = to_float(os.getenv("TOP_P", "1.0"))
DEFAULT_TIMEOUT = to_float(os.getenv("TIMEOUT", "32400.0"))
DEFAULT_TOOL_TIMEOUT = to_float(os.getenv("TOOL_TIMEOUT", "32400.0"))
DEFAULT_PARALLEL_TOOL_CALLS = to_boolean(os.getenv("PARALLEL_TOOL_CALLS", "True"))
DEFAULT_SEED = to_integer(os.getenv("SEED", None))
DEFAULT_PRESENCE_PENALTY = to_float(os.getenv("PRESENCE_PENALTY", "0.0"))
DEFAULT_FREQUENCY_PENALTY = to_float(os.getenv("FREQUENCY_PENALTY", "0.0"))
DEFAULT_LOGIT_BIAS = to_dict(os.getenv("LOGIT_BIAS", None))
DEFAULT_STOP_SEQUENCES = to_list(os.getenv("STOP_SEQUENCES", None))
DEFAULT_EXTRA_HEADERS = to_dict(os.getenv("EXTRA_HEADERS", None))
DEFAULT_EXTRA_BODY = to_dict(os.getenv("EXTRA_BODY", None))

AGENT_NAME = "AdGuardHome"
AGENT_DESCRIPTION = "A multi-agent system for managing AdGuard Home resources via delegated specialists."


SUPERVISOR_SYSTEM_PROMPT = os.environ.get(
    "SUPERVISOR_SYSTEM_PROMPT",
    default=(
        "You are the AdGuard Home Supervisor Agent.\n"
        "Your goal is to assist the user by assigning tasks to specialized child agents through your available toolset.\n"
        "Analyze the user's request and determine which domain(s) it falls into (e.g., devices, dns, stats, filter lists, etc.).\n"
        "Then, call the appropriate tool(s) to delegate the task.\n"
        "Synthesize the results from the child agents into a final helpful response.\n"
        "Always be warm, professional, and helpful."
        "Note: The final response should contain all the relevant information from the tool executions. Never leave out any relevant information or leave it to the user to find it. "
        "You are the final authority on the user's request and the final communicator to the user. Present information as logically and concisely as possible. "
        "Explore using organized output with headers, sections, lists, and tables to make the information easy to navigate. "
        "If there are gaps in the information, clearly state that information is missing. Do not make assumptions or invent placeholder information, only use the information which is available."
    ),
)

ACCOUNT_PROMPT = os.environ.get(
    "ACCOUNT_PROMPT",
    default=(
        "You are the AdGuard Home Account Agent.\n"
        "Your goal is to manage account limits and authentication.\n"
    ),
)

DEVICES_PROMPT = os.environ.get(
    "DEVICES_PROMPT",
    default=(
        "You are the AdGuard Home Devices Agent.\n"
        "Your goal is to manage devices that use AdGuard Home.\n"
        "You can:\n"
        "- CRUD: `create_device`, `get_device`, `update_device`, `delete_device`\n"
        "- List: `list_devices`\n"
    ),
)

DNS_PROMPT = os.environ.get(
    "DNS_PROMPT",
    default=(
        "You are the AdGuard Home DNS Agent.\n"
        "Your goal is to manage DNS servers and configuration.\n"
        "You can:\n"
        "- Config: `get_dns_info`, `set_dns_config`\n"
        "- Upstreams: `test_upstream_dns`\n"
        "- Protection: `set_protection`\n"
        "- Cache: `clear_cache`\n"
    ),
)

FILTERING_PROMPT = os.environ.get(
    "FILTERING_PROMPT",
    default=(
        "You are the AdGuard Home Filtering Agent.\n"
        "Your goal is to manage filtering rules and status.\n"
        "You can:\n"
        "- Status: `get_filtering_status`, `set_filtering_config`\n"
        "- Rules: `set_filtering_rules`\n"
        "- Filters: `add_filter_url`, `remove_filter_url`, `set_filter_url_params`, `refresh_filters`\n"
        "- Check: `check_host_filtering`\n"
    ),
)

QUERY_LOG_PROMPT = os.environ.get(
    "QUERY_LOG_PROMPT",
    default=(
        "You are the AdGuard Home Query Log Agent.\n"
        "Your goal is to manage and retrieve query logs.\n"
        "You can:\n"
        "- Get: `get_query_log`\n"
        "- Config: `get_query_log_config`, `set_query_log_config`\n"
        "- Clear: `clear_query_log`\n"
    ),
)

STATS_PROMPT = os.environ.get(
    "STATS_PROMPT",
    default=(
        "You are the AdGuard Home Statistics Agent.\n"
        "Your goal is to retrieve and manage statistics.\n"
        "You can:\n"
        "- Get: `get_stats`\n"
        "- Config: `get_stats_config`, `set_stats_config`\n"
        "- Reset: `reset_stats`\n"
    ),
)


ACCESS_PROMPT = os.environ.get(
    "ACCESS_PROMPT",
    default=(
        "You are the AdGuard Home Access Agent.\n"
        "Your goal is to manage access lists.\n"
        "You can:\n"
        "- Get: `access_list`\n"
        "- Set: `set_access_list`\n"
    ),
)


BLOCKED_SERVICES_PROMPT = os.environ.get(
    "BLOCKED_SERVICES_PROMPT",
    default=(
        "You are the AdGuard Home Blocked Services Agent.\n"
        "Your goal is to manage blocked services.\n"
        "You can:\n"
        "- List: `get_all_blocked_services`, `get_blocked_services_list`\n"
        "- Update: `update_blocked_services`\n"
    ),
)


CLIENTS_PROMPT = os.environ.get(
    "CLIENTS_PROMPT",
    default=(
        "You are the AdGuard Home Clients Agent.\n"
        "Your goal is to manage clients.\n"
        "You can:\n"
        "- List: `list_clients`\n"
        "- Search: `search_clients`\n"
        "- CRUD: `add_client`, `update_client`, `delete_client`\n"
    ),
)


DHCP_PROMPT = os.environ.get(
    "DHCP_PROMPT",
    default=(
        "You are the AdGuard Home DHCP Agent.\n"
        "Your goal is to manage DHCP status and configuration.\n"
        "You can:\n"
        "- Gateway: `get_dhcp_status`, `set_dhcp_config`, `reset_dhcp`, `reset_dhcp_leases`\n"
        "- Interfaces: `get_dhcp_interfaces`, `find_active_dhcp`\n"
        "- Leases: `add_dhcp_static_lease`, `remove_dhcp_static_lease`, `update_dhcp_static_lease`\n"
    ),
)


REWRITES_PROMPT = os.environ.get(
    "REWRITES_PROMPT",
    default=(
        "You are the AdGuard Home Rewrites Agent.\n"
        "Your goal is to manage DNS rewrites.\n"
        "You can:\n"
        "- List: `list_rewrites`\n"
        "- Settings: `get_rewrite_settings`, `update_rewrite_settings`\n"
        "- CRUD: `add_rewrite`, `update_rewrite`, `delete_rewrite`\n"
    ),
)


SETTINGS_PROMPT = os.environ.get(
    "SETTINGS_PROMPT",
    default=(
        "You are the AdGuard Home Settings Agent.\n"
        "Your goal is to manage various settings (SafeBrowsing, SafeSearch, Parental Control).\n"
        "You can:\n"
        "- SafeBrowsing: `get_safebrowsing_status`, `enable_safebrowsing`, `disable_safebrowsing`\n"
        "- SafeSearch: `get_safesearch_status`, `update_safesearch_settings`\n"
        "- Parental: `get_parental_status`, `enable_parental_control`, `disable_parental_control`\n"
    ),
)


SYSTEM_PROMPT = os.environ.get(
    "SYSTEM_PROMPT",
    default=(
        "You are the AdGuard Home System Agent.\n"
        "Your goal is to retrieve system information.\n"
        "You can:\n"
        "- Get: `get_version`\n"
    ),
)

PROFILE_PROMPT = os.environ.get(
    "PROFILE_PROMPT",
    default=(
        "You are the AdGuard Home Profile Agent.\n"
        "Your goal is to manage the current user profile.\n"
        "You can:\n"
        "- Get: `get_profile`\n"
        "- Update: `update_profile`\n"
    ),
)

TLS_PROMPT = os.environ.get(
    "TLS_PROMPT",
    default=(
        "You are the AdGuard Home TLS Agent.\n"
        "Your goal is to manage TLS configuration.\n"
        "You can:\n"
        "- Status: `get_tls_status`\n"
        "- Config: `configure_tls`, `validate_tls`\n"
    ),
)

MOBILE_PROMPT = os.environ.get(
    "MOBILE_PROMPT",
    default=(
        "You are the AdGuard Home Mobile Config Agent.\n"
        "Your goal is to retrieve mobile configuration files.\n"
        "You can:\n"
        "- Get: `get_doh_mobile_config`, `get_dot_mobile_config`\n"
    ),
)


def create_agent(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = DEFAULT_LLM_BASE_URL,
    api_key: Optional[str] = DEFAULT_LLM_API_KEY,
    mcp_url: str = DEFAULT_MCP_URL,
    mcp_config: str = DEFAULT_MCP_CONFIG,
    custom_skills_directory: Optional[str] = DEFAULT_CUSTOM_SKILLS_DIRECTORY,
    ssl_verify: bool = DEFAULT_SSL_VERIFY,
) -> Agent:
    """
    Creates the Supervisor Agent with sub-agents registered as tools.
    """
    logger.info("Initializing Multi-Agent System for AdGuard Home...")

    model = create_model(
        provider=provider,
        model_id=model_id,
        base_url=base_url,
        api_key=api_key,
        ssl_verify=ssl_verify,
        timeout=DEFAULT_TIMEOUT,
    )
    settings = ModelSettings(
        max_tokens=DEFAULT_MAX_TOKENS,
        temperature=DEFAULT_TEMPERATURE,
        top_p=DEFAULT_TOP_P,
        timeout=DEFAULT_TIMEOUT,
        parallel_tool_calls=DEFAULT_PARALLEL_TOOL_CALLS,
        seed=DEFAULT_SEED,
        presence_penalty=DEFAULT_PRESENCE_PENALTY,
        frequency_penalty=DEFAULT_FREQUENCY_PENALTY,
        logit_bias=DEFAULT_LOGIT_BIAS,
        stop_sequences=DEFAULT_STOP_SEQUENCES,
        extra_headers=DEFAULT_EXTRA_HEADERS,
        extra_body=DEFAULT_EXTRA_BODY,
    )

    agent_toolsets = []
    if mcp_url:
        if "sse" in mcp_url.lower():
            server = MCPServerSSE(
                mcp_url,
                http_client=httpx.AsyncClient(
                    verify=ssl_verify, timeout=DEFAULT_TIMEOUT
                ),
            )
        else:
            server = MCPServerStreamableHTTP(
                mcp_url,
                http_client=httpx.AsyncClient(
                    verify=ssl_verify, timeout=DEFAULT_TIMEOUT
                ),
            )
        agent_toolsets.append(server)
        logger.info(f"Connected to MCP Server: {mcp_url}")
    elif mcp_config:
        mcp_toolset = load_mcp_servers(mcp_config)
        for server in mcp_toolset:
            if hasattr(server, "http_client"):
                server.http_client = httpx.AsyncClient(
                    verify=ssl_verify, timeout=DEFAULT_TIMEOUT
                )
        agent_toolsets.extend(mcp_toolset)
        logger.info(f"Connected to MCP Config JSON: {mcp_toolset}")

    # Skills are loaded per-agent based on tags

    agent_defs = {
        "access": (ACCESS_PROMPT, "AdGuardHome_Access_Agent"),
        "account": (ACCOUNT_PROMPT, "AdGuardHome_Account_Agent"),
        "blocked_services": (
            BLOCKED_SERVICES_PROMPT,
            "AdGuardHome_Blocked_Services_Agent",
        ),
        "clients": (CLIENTS_PROMPT, "AdGuardHome_Clients_Agent"),
        "dhcp": (DHCP_PROMPT, "AdGuardHome_DHCP_Agent"),
        "filtering": (FILTERING_PROMPT, "AdGuardHome_Filtering_Agent"),
        "query_log": (QUERY_LOG_PROMPT, "AdGuardHome_Query_Log_Agent"),
        "rewrites": (REWRITES_PROMPT, "AdGuardHome_Rewrites_Agent"),
        "settings": (SETTINGS_PROMPT, "AdGuardHome_Settings_Agent"),
        "stats": (STATS_PROMPT, "AdGuardHome_Stats_Agent"),
        "system": (SYSTEM_PROMPT, "AdGuardHome_System_Agent"),
        "profile": (PROFILE_PROMPT, "AdGuardHome_Profile_Agent"),
        "tls": (TLS_PROMPT, "AdGuardHome_TLS_Agent"),
        "mobile": (MOBILE_PROMPT, "AdGuardHome_Mobile_Agent"),
    }

    child_agents = {}

    for tag, (system_prompt, agent_name) in agent_defs.items():
        tag_toolsets = []
        for ts in agent_toolsets:
            logger.info(f"Reviewing toolset: {ts}")

            def filter_func(ctx, tool_def, t=tag):
                return tool_in_tag(tool_def, t)

            if hasattr(ts, "filtered"):
                filtered_ts = ts.filtered(filter_func)
                logger.info(f"Inspecting tool: {filtered_ts}")
                tag_toolsets.append(filtered_ts)
            else:
                pass

        skill_dir_name = f"adguard-{tag.replace('_', '-')}"

        # Check custom skills directory
        if custom_skills_directory:
            skill_dir_path = os.path.join(custom_skills_directory, skill_dir_name)
            if os.path.exists(skill_dir_path):
                tag_toolsets.append(SkillsToolset(directories=[skill_dir_path]))
                logger.info(
                    f"Loaded specialized skills for {tag} from {skill_dir_path}"
                )

        # Check default skills directory
        default_skill_path = os.path.join(get_skills_path(), skill_dir_name)
        if os.path.exists(default_skill_path):
            tag_toolsets.append(SkillsToolset(directories=[default_skill_path]))
            logger.info(
                f"Loaded specialized skills for {tag} from {default_skill_path}"
            )

        # Collect tool names for logging
        all_tool_names = []
        for ts in tag_toolsets:
            try:
                # Unwrap FilteredToolset
                current_ts = ts
                while hasattr(current_ts, "wrapped"):
                    current_ts = current_ts.wrapped

                # Check for .tools (e.g. SkillsToolset)
                if hasattr(current_ts, "tools") and isinstance(current_ts.tools, dict):
                    all_tool_names.extend(current_ts.tools.keys())
                # Check for ._tools (some implementations might use private attr)
                elif hasattr(current_ts, "_tools") and isinstance(
                    current_ts._tools, dict
                ):
                    all_tool_names.extend(current_ts._tools.keys())
                else:
                    # Fallback for MCP or others where tools are not available sync
                    all_tool_names.append(f"<{type(current_ts).__name__}>")
            except Exception as e:
                logger.info(f"Unable to retrieve toolset: {e}")
                pass

        tool_list_str = ", ".join(all_tool_names)
        logger.info(f"Available tools for {agent_name} ({tag}): {tool_list_str}")
        agent = Agent(
            name=agent_name,
            system_prompt=system_prompt,
            model=model,
            model_settings=settings,
            toolsets=tag_toolsets,
            tool_timeout=DEFAULT_TOOL_TIMEOUT,
        )
        child_agents[tag] = agent

    supervisor = Agent(
        name=AGENT_NAME,
        system_prompt=SUPERVISOR_SYSTEM_PROMPT,
        model=model,
        model_settings=settings,
        deps_type=Any,
    )

    @supervisor.tool
    async def assign_task_to_account_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to account limits to the Account Agent."""
        return (
            await child_agents["account"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_filtering_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to filter lists to the Filtering Agent."""
        return (
            await child_agents["filtering"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_query_log_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to query logs to the Query Log Agent."""
        return (
            await child_agents["query_log"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_stats_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to statistics to the Stats Agent."""
        return (
            await child_agents["stats"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_access_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to access lists to the Access Agent."""
        return (
            await child_agents["access"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_blocked_services_agent(
        ctx: RunContext[Any], task: str
    ) -> str:
        """Assign a task related to blocked services to the Blocked Services Agent."""
        return (
            await child_agents["blocked_services"].run(
                task, usage=ctx.usage, deps=ctx.deps
            )
        ).output

    @supervisor.tool
    async def assign_task_to_clients_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to clients to the Clients Agent."""
        return (
            await child_agents["clients"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_dhcp_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to DHCP to the DHCP Agent."""
        return (
            await child_agents["dhcp"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_rewrites_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to DNS rewrites to the Rewrites Agent."""
        return (
            await child_agents["rewrites"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_settings_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to settings (SafeBrowsing, SafeSearch, Parental) to the Settings Agent."""
        return (
            await child_agents["settings"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_system_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to system information to the System Agent."""
        return (
            await child_agents["system"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_profile_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to user profile to the Profile Agent."""
        return (
            await child_agents["profile"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_tls_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to TLS configuration to the TLS Agent."""
        return (
            await child_agents["tls"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_mobile_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to mobile configuration to the Mobile Agent."""
        return (
            await child_agents["mobile"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    return supervisor


def create_agent_server(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = DEFAULT_LLM_BASE_URL,
    api_key: Optional[str] = DEFAULT_LLM_API_KEY,
    mcp_url: str = DEFAULT_MCP_URL,
    mcp_config: str = DEFAULT_MCP_CONFIG,
    custom_skills_directory: Optional[str] = DEFAULT_CUSTOM_SKILLS_DIRECTORY,
    debug: Optional[bool] = DEFAULT_DEBUG,
    host: Optional[str] = DEFAULT_HOST,
    port: Optional[int] = DEFAULT_PORT,
    enable_web_ui: bool = DEFAULT_ENABLE_WEB_UI,
    ssl_verify: bool = DEFAULT_SSL_VERIFY,
):
    print(
        f"Starting {AGENT_NAME}:"
        f"\tprovider={provider}"
        f"\tmodel={model_id}"
        f"\tbase_url={base_url}"
        f"\tmcp={mcp_url} | {mcp_config}"
        f"\tssl_verify={ssl_verify}"
    )
    agent = create_agent(
        provider=provider,
        model_id=model_id,
        base_url=base_url,
        api_key=api_key,
        mcp_url=mcp_url,
        mcp_config=mcp_config,
        custom_skills_directory=custom_skills_directory,
        ssl_verify=ssl_verify,
    )

    # Always load default skills

    skills = load_skills_from_directory(get_skills_path())

    logger.info(f"Loaded {len(skills)} default skills from {get_skills_path()}")

    # Load custom skills if provided

    if custom_skills_directory and os.path.exists(custom_skills_directory):

        custom_skills = load_skills_from_directory(custom_skills_directory)

        skills.extend(custom_skills)

        logger.info(
            f"Loaded {len(custom_skills)} custom skills from {custom_skills_directory}"
        )

    if not skills:

        skills = [
            Skill(
                id="adguard_home_agent",
                name="AdGuard Home Agent",
                description="General access to AdGuard Home tools",
                tags=["adguard-home"],
                input_modes=["text"],
                output_modes=["text"],
            )
        ]

    a2a_app = agent.to_a2a(
        name=AGENT_NAME,
        description=AGENT_DESCRIPTION,
        version=__version__,
        skills=skills,
        debug=debug,
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if hasattr(a2a_app, "router") and hasattr(a2a_app.router, "lifespan_context"):
            async with a2a_app.router.lifespan_context(a2a_app):
                yield
        else:
            yield

    app = FastAPI(
        title=f"{AGENT_NAME} - A2A + AG-UI Server",
        description=AGENT_DESCRIPTION,
        debug=debug,
        lifespan=lifespan,
    )

    @app.get("/health")
    async def health_check():
        return {"status": "OK"}

    app.mount("/a2a", a2a_app)

    @app.post("/ag-ui")
    async def ag_ui_endpoint(request: Request) -> Response:
        accept = request.headers.get("accept", SSE_CONTENT_TYPE)
        try:
            run_input = AGUIAdapter.build_run_input(await request.body())
        except ValidationError as e:
            return Response(
                content=json.dumps(e.json()),
                media_type="application/json",
                status_code=422,
            )

        if hasattr(run_input, "messages"):
            run_input.messages = prune_large_messages(run_input.messages)

        adapter = AGUIAdapter(agent=agent, run_input=run_input, accept=accept)
        event_stream = adapter.run_stream()
        sse_stream = adapter.encode_stream(event_stream)

        return StreamingResponse(
            sse_stream,
            media_type=accept,
        )

    if enable_web_ui:
        web_ui = agent.to_web(instructions=SUPERVISOR_SYSTEM_PROMPT)
        app.mount("/", web_ui)
        logger.info(
            "Starting server on %s:%s (A2A at /a2a, AG-UI at /ag-ui, Web UI: %s)",
            host,
            port,
            "Enabled at /" if enable_web_ui else "Disabled",
        )

    uvicorn.run(
        app,
        host=host,
        port=port,
        timeout_keep_alive=1800,
        timeout_graceful_shutdown=60,
        log_level="debug" if debug else "info",
    )


def agent_server():
    print(f"adguard_home_agent v{__version__}")
    parser = argparse.ArgumentParser(
        add_help=False, description=f"Run the {AGENT_NAME} A2A + AG-UI Server"
    )
    parser.add_argument(
        "--host", default=DEFAULT_HOST, help="Host to bind the server to"
    )
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT, help="Port to bind the server to"
    )
    parser.add_argument("--debug", type=bool, default=DEFAULT_DEBUG, help="Debug mode")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")

    parser.add_argument(
        "--provider",
        default=DEFAULT_PROVIDER,
        choices=["openai", "anthropic", "google", "huggingface"],
        help="LLM Provider",
    )
    parser.add_argument("--model-id", default=DEFAULT_MODEL_ID, help="LLM Model ID")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_LLM_BASE_URL,
        help="LLM Base URL (for OpenAI compatible providers)",
    )
    parser.add_argument("--api-key", default=DEFAULT_LLM_API_KEY, help="LLM API Key")
    parser.add_argument("--mcp-url", default=DEFAULT_MCP_URL, help="MCP Server URL")
    parser.add_argument(
        "--mcp-config", default=DEFAULT_MCP_CONFIG, help="MCP Server Config"
    )
    parser.add_argument(
        "--custom-skills-directory",
        default=DEFAULT_CUSTOM_SKILLS_DIRECTORY,
        help="Directory containing additional custom agent skills",
    )
    parser.add_argument(
        "--web",
        action="store_true",
        default=DEFAULT_ENABLE_WEB_UI,
        help="Enable Pydantic AI Web UI",
    )

    parser.add_argument(
        "--insecure",
        action="store_true",
        help="Disable SSL verification for LLM requests (Use with caution)",
    )
    parser.add_argument("--help", action="store_true", help="Show usage")

    args = parser.parse_args()

    if hasattr(args, "help") and args.help:
        usage()
        sys.exit(0)

    if args.debug:
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.StreamHandler()],
            force=True,
        )
        logging.getLogger("pydantic_ai").setLevel(logging.DEBUG)
        logging.getLogger("fastmcp").setLevel(logging.DEBUG)
        logging.getLogger("httpcore").setLevel(logging.DEBUG)
        logging.getLogger("httpx").setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")

    create_agent_server(
        provider=args.provider,
        model_id=args.model_id,
        base_url=args.base_url,
        api_key=args.api_key,
        mcp_url=args.mcp_url,
        mcp_config=args.mcp_config,
        custom_skills_directory=args.custom_skills_directory,
        debug=args.debug,
        host=args.host,
        port=args.port,
        enable_web_ui=args.web,
        ssl_verify=not args.insecure,
    )


def usage():
    print(
        f"AdGuard Home Agent ({__version__}): CLI Tool\n\n"
        "Usage:\n"
        "--host                [ Host to bind the server to ]\n"
        "--port                [ Port to bind the server to ]\n"
        "--debug               [ Debug mode ]\n"
        "--reload              [ Enable auto-reload ]\n"
        "--provider            [ LLM Provider ]\n"
        "--model-id            [ LLM Model ID ]\n"
        "--base-url            [ LLM Base URL (for OpenAI compatible providers) ]\n"
        "--api-key             [ LLM API Key ]\n"
        "--mcp-url             [ MCP Server URL ]\n"
        "--mcp-config          [ MCP Server Config ]\n"
        "--custom-skills-directory    [ Directory containing additional custom agent skills ]\n"
        "--web                 [ Enable Pydantic AI Web UI ]\n"
        "\n"
        "Examples:\n"
        "  [Simple]  adguard-home-agent \n"
        '  [Complex] adguard-home-agent --host "value" --port "value" --debug "value" --reload --provider "value" --model-id "value" --base-url "value" --api-key "value" --mcp-url "value" --mcp-config "value" --custom-skills-directory "value" --web\n'
    )


if __name__ == "__main__":
    agent_server()
