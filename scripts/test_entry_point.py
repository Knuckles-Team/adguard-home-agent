import sys
import os
from pathlib import Path
import inspect


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# agents/adguard-home-agent/scripts/
WORKSPACE_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
# agent-packages/

sys.path.append(os.path.join(WORKSPACE_ROOT, "agent-utilities"))

import agent_utilities.base_utilities as bu

def simulate_entry_point():
    print(f"Executing File: {__file__}")
    print(f"CWD: {os.getcwd()}")


    pkg = bu.retrieve_package_name()
    print(f"Retrieved Package Name (from __main__): {pkg}")

if __name__ == "__main__":
    simulate_entry_point()
