# run_all.py

import subprocess
import os
import sys
import traceback

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "src")

scripts = [
    "spread_logger.py",
    "usdt_premium_logger.py",
    "mempool_logger.py",
    "score_logger.py"
]

# Run logger scripts
for script in scripts:
    script_path = os.path.join(SCRIPTS_DIR, script)
    print(f"\n--- Running {script_path} ---")
    try:
        result = subprocess.run(
            ["python", script_path],
            env={**os.environ, "PYTHONPATH": BASE_DIR},
            check=True,
            text=True
        )
        print(f"✅ {script} succeeded")
    except subprocess.CalledProcessError as e:
        print(f"❌ {script} failed with return code {e.returncode}")
        print(e.output if e.output else "No output captured.")
    except Exception as e:
        print(f"❌ Exception while running {script}: {e}")
        traceback.print_exc()

# Run analysis steps directly
try:
    print("\n--- Generating forward return table ---")
    from src.analyzer import generate_forward_return_table
    generate_forward_return_table()
except Exception:
    print("❌ Error in generate_forward_return_table():")
    traceback.print_exc()

try:
    print("\n--- Reconstructing implied BTC/XMR spread ---")
    from src.analyzer import analyze_implied_xmr_btc_spread
    analyze_implied_xmr_btc_spread()
except Exception:
    print("❌ Error in analyze_implied_xmr_btc_spread():")
    traceback.print_exc()
