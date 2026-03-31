import sys
import os
from pathlib import Path
import inspect


sys.path.append("/home/genius/Workspace/agent-packages/agent-utilities")

import agent_utilities.base_utilities as bu

def simulate_entry_point():
    print(f"Executing File: {__file__}")
    print(f"CWD: {os.getcwd()}")


    pkg = bu.retrieve_package_name()
    print(f"Retrieved Package Name (from __main__): {pkg}")

if __name__ == "__main__":
    simulate_entry_point()
