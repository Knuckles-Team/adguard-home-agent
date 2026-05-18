import sys
import traceback

print("Step 1: Start", file=sys.stderr)
try:
    print("Step 2: Before import agent_utilities", file=sys.stderr)
    print("Step 3: After import agent_utilities", file=sys.stderr)
except SystemExit as e:
    print(f"SystemExit caught! Code: {e.code}", file=sys.stderr)
except Exception as e:
    print(f"Exception caught: {e}", file=sys.stderr)
    traceback.print_exc()
print("Step 4: End", file=sys.stderr)
