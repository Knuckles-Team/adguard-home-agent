
import re
from pathlib import Path

def get_mcp_tools():
    tools = []
    mcp_file = Path("adguard_home_agent/adguard_mcp_server.py")
    content = mcp_file.read_text()

                         
                                 
                                   

                                                              
                                   

    lines = content.split('\n')
    for i, line in enumerate(lines):
        if "@mcp.tool" in line:
                                
            for j in range(i+1, len(lines)):
                if "def " in lines[j]:
                    func_name = lines[j].split("def ")[1].split("(")[0].strip()
                    tag_match = re.search(r'tags=\{("|\')(.+?)("|\')\}', line)
                    tag = tag_match.group(2) if tag_match else "unknown"
                    tools.append((func_name, tag))
                    break
    return tools

def get_skill_tools():
    skills_dir = Path("adguard_home_agent/skills")
    skill_tools = {}

    for skill_file in skills_dir.rglob("SKILL.md"):
        content = skill_file.read_text()
                                                        
                                                      

                                                               
        skill_name = skill_file.parent.name
        skill_tools[skill_name] = content

    return skill_tools

def verify():
    mcp_tools = get_mcp_tools()
    skill_tools_map = get_skill_tools()

    missing = []

    for tool, tag in mcp_tools:
                                                       
                                             

                                                                   
        found = False
        for skill_name, content in skill_tools_map.items():
            if tool in content:
                found = True
                break

        if not found:
            missing.append((tool, tag))

    print(f"Found {len(mcp_tools)} tools in mcp_server.py")
    if missing:
        print("Missing tools:")
        for tool, tag in missing:
            print(f"- {tool} (tag: {tag})")
    else:
        print("All tools found in SKILL.md files.")

if __name__ == "__main__":
    verify()
