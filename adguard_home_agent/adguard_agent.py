#!/usr/bin/env python
# coding: utf-8

import sys
import json
import os
import argparse
import logging
import uvicorn
from typing import Optional, Any
from contextlib import asynccontextmanager

from pydantic_ai import Agent, ModelSettings, RunContext
from pydantic_ai.mcp import load_mcp_servers, MCPServerStreamableHTTP, MCPServerSSE
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

__version__ = "0.1.1"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # Output to console
)
logging.getLogger("pydantic_ai").setLevel(logging.INFO)
logging.getLogger("fastmcp").setLevel(logging.INFO)
logging.getLogger("httpx").setLevel(logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_HOST = os.getenv("HOST", "0.0.0.0")
DEFAULT_PORT = to_integer(string=os.getenv("PORT", "9000"))
DEFAULT_DEBUG = to_boolean(string=os.getenv("DEBUG", "False"))
DEFAULT_PROVIDER = os.getenv("PROVIDER", "openai")
DEFAULT_MODEL_ID = os.getenv("MODEL_ID", "qwen/qwen3-4b-2507")
DEFAULT_OPENAI_BASE_URL = os.getenv(
    "OPENAI_BASE_URL", "http://host.docker.internal:1234/v1"
)
DEFAULT_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "ollama")
DEFAULT_MCP_URL = os.getenv("MCP_URL", None)
DEFAULT_MCP_CONFIG = os.getenv("MCP_CONFIG", get_mcp_config_path())
DEFAULT_SKILLS_DIRECTORY = os.getenv("SKILLS_DIRECTORY", get_skills_path())
DEFAULT_ENABLE_WEB_UI = to_boolean(os.getenv("ENABLE_WEB_UI", "False"))

# Model Settings
DEFAULT_MAX_TOKENS = to_integer(os.getenv("MAX_TOKENS", "8192"))
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

# -------------------------------------------------------------------------
# 1. System Prompts
# -------------------------------------------------------------------------

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
        "Your goal is to manage DNS servers.\n"
        "You can:\n"
        "- CRUD: `create_dns_server`, `get_dns_server`, `update_dns_server`, `delete_dns_server`\n"
        "- List: `list_dns_servers`\n"
    ),
)

FILTERING_PROMPT = os.environ.get(
    "FILTERING_PROMPT",
    default=(
        "You are the AdGuard Home Filtering Agent.\n"
        "Your goal is to manage filter lists.\n"
        "You can:\n"
        "- List: `list_filter_lists`\n"
    ),
)

QUERY_LOG_PROMPT = os.environ.get(
    "QUERY_LOG_PROMPT",
    default=(
        "You are the AdGuard Home Query Log Agent.\n"
        "Your goal is to retrieve query logs.\n"
        "You can:\n"
        "- Get: `get_query_log`\n"
    ),
)

STATS_PROMPT = os.environ.get(
    "STATS_PROMPT",
    default=(
        "You are the AdGuard Home Statistics Agent.\n"
        "Your goal is to retrieve statistics.\n"
        "You can:\n"
        "- Get: `get_stats_categories`, `get_stats_companies`, `get_stats_countries`, `get_stats_devices`, `get_stats_domains`, `get_stats_time`\n"
    ),
)


# -------------------------------------------------------------------------
# 2. Agent Creation Logic
# -------------------------------------------------------------------------


def create_agent(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    mcp_url: str = DEFAULT_MCP_URL,
    mcp_config: str = DEFAULT_MCP_CONFIG,
    skills_directory: Optional[str] = DEFAULT_SKILLS_DIRECTORY,
) -> Agent:
    """
    Creates the Supervisor Agent with sub-agents registered as tools.
    """
    logger.info("Initializing Multi-Agent System for AdGuard Home...")

    model = create_model(provider, model_id, base_url, api_key)
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

    # Load master toolsets
    master_toolsets = []
    if mcp_config:
        mcp_toolset = load_mcp_servers(mcp_config)
        master_toolsets.extend(mcp_toolset)
        logger.info(f"Connected to MCP Config JSON: {mcp_toolset}")
    elif mcp_url:
        if "sse" in mcp_url.lower():
            server = MCPServerSSE(mcp_url)
        else:
            server = MCPServerStreamableHTTP(mcp_url)
        master_toolsets.append(server)
        logger.info(f"Connected to MCP Server: {mcp_url}")

    if skills_directory and os.path.exists(skills_directory):
        master_toolsets.append(SkillsToolset(directories=[str(skills_directory)]))

    # Define Tag -> Prompt map
    agent_defs = {
        "account": (ACCOUNT_PROMPT, "AdGuardHome_Account_Agent"),
        "devices": (DEVICES_PROMPT, "AdGuardHome_Devices_Agent"),
        "dns": (DNS_PROMPT, "AdGuardHome_DNS_Agent"),
        "filtering": (FILTERING_PROMPT, "AdGuardHome_Filtering_Agent"),
        "query_log": (QUERY_LOG_PROMPT, "AdGuardHome_Query_Log_Agent"),
        "stats": (STATS_PROMPT, "AdGuardHome_Stats_Agent"),
    }

    child_agents = {}

    for tag, (system_prompt, agent_name) in agent_defs.items():
        tag_toolsets = []
        for ts in master_toolsets:

            def filter_func(ctx, tool_def, t=tag):
                return tool_in_tag(tool_def, t)

            if hasattr(ts, "filtered"):
                filtered_ts = ts.filtered(filter_func)
                tag_toolsets.append(filtered_ts)
            else:
                pass

        agent = Agent(
            name=agent_name,
            system_prompt=system_prompt,
            model=model,
            model_settings=settings,
            toolsets=tag_toolsets,
            tool_timeout=DEFAULT_TOOL_TIMEOUT,
        )
        child_agents[tag] = agent

    # Create Supervisor
    supervisor = Agent(
        name=AGENT_NAME,
        system_prompt=SUPERVISOR_SYSTEM_PROMPT,
        model=model,
        model_settings=settings,
        deps_type=Any,
    )

    # Define delegation tools

    @supervisor.tool
    async def assign_task_to_account_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to account limits to the Account Agent."""
        return (
            await child_agents["account"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_devices_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to devices to the Devices Agent."""
        return (
            await child_agents["devices"].run(task, usage=ctx.usage, deps=ctx.deps)
        ).output

    @supervisor.tool
    async def assign_task_to_dns_agent(ctx: RunContext[Any], task: str) -> str:
        """Assign a task related to DNS servers to the DNS Agent."""
        return (
            await child_agents["dns"].run(task, usage=ctx.usage, deps=ctx.deps)
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

    return supervisor


def create_agent_server(
    provider: str = DEFAULT_PROVIDER,
    model_id: str = DEFAULT_MODEL_ID,
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    mcp_url: str = DEFAULT_MCP_URL,
    mcp_config: str = DEFAULT_MCP_CONFIG,
    skills_directory: Optional[str] = DEFAULT_SKILLS_DIRECTORY,
    debug: Optional[bool] = DEFAULT_DEBUG,
    host: Optional[str] = DEFAULT_HOST,
    port: Optional[int] = DEFAULT_PORT,
    enable_web_ui: bool = DEFAULT_ENABLE_WEB_UI,
):
    print(
        f"Starting {AGENT_NAME} with provider={provider}, model={model_id}, mcp={mcp_url} | {mcp_config}"
    )
    agent = create_agent(
        provider=provider,
        model_id=model_id,
        base_url=base_url,
        api_key=api_key,
        mcp_url=mcp_url,
        mcp_config=mcp_config,
        skills_directory=skills_directory,
    )

    if skills_directory and os.path.exists(skills_directory):
        skills = load_skills_from_directory(skills_directory)
        logger.info(f"Loaded {len(skills)} skills from {skills_directory}")
    else:
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
        if hasattr(a2a_app, "router"):
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

        # Prune large messages from history
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
        default=DEFAULT_OPENAI_BASE_URL,
        help="LLM Base URL (for OpenAI compatible providers)",
    )
    parser.add_argument("--api-key", default=DEFAULT_OPENAI_API_KEY, help="LLM API Key")
    parser.add_argument("--mcp-url", default=DEFAULT_MCP_URL, help="MCP Server URL")
    parser.add_argument(
        "--mcp-config", default=DEFAULT_MCP_CONFIG, help="MCP Server Config"
    )
    parser.add_argument(
        "--skills-directory",
        default=DEFAULT_SKILLS_DIRECTORY,
        help="Directory containing agent skills",
    )
    parser.add_argument(
        "--web",
        action="store_true",
        default=DEFAULT_ENABLE_WEB_UI,
        help="Enable Pydantic AI Web UI",
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
        skills_directory=args.skills_directory,
        debug=args.debug,
        host=args.host,
        port=args.port,
        enable_web_ui=args.web,
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
        "--skills-directory    [ Directory containing agent skills ]\n"
        "--web                 [ Enable Pydantic AI Web UI ]\n"
        "\n"
        "Examples:\n"
        "  [Simple]  adguard-home-agent \n"
        '  [Complex] adguard-home-agent --host "value" --port "value" --debug "value" --reload --provider "value" --model-id "value" --base-url "value" --api-key "value" --mcp-url "value" --mcp-config "value" --skills-directory "value" --web\n'
    )


if __name__ == "__main__":
    agent_server()
