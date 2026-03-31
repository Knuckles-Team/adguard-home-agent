import asyncio
import os
from agent_utilities.agent_utilities import create_agent

os.environ["ADGUARD_URL"] = "http://localhost:3000"                              
os.environ["ADGUARD_USERNAME"] = "admin"
os.environ["ADGUARD_PASSWORD"] = "admin"

async def main():
    agent = create_agent(
        name="Test Adguard",
        system_prompt="""You have access to the `mcp-client` skill.
Please use `run_skill_script` with `skill_name="mcp-client"`, `script_name="scripts/mcp_client.py"`, and `args={"config": "../references/adguard-home-agent.json", "action": "list-mcp-tools"}` to list the tools in the AdGuard Home MCP server.
Tell me what tools are available and what the first tool is."""
    )
                                                                              
    result = await agent.run("List the adguard tools.")
    print("Agent Output:\n", result.data)

if __name__ == "__main__":
    asyncio.run(main())
