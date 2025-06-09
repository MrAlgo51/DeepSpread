import subprocess
import os
import sys

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
    subprocess.run(["python", script_path], env={**os.environ, "PYTHONPATH": BASE_DIR})

# Run analysis functions directly (no subprocess needed)
print("\n--- Generating forward return table ---")
from src.analyzer import generate_forward_return_table
generate_forward_return_table()

print("\n--- Reconstructing implied BTC/XMR spread ---")
from src.analyzer import analyze_implied_xmr_btc_spread
analyze_implied_xmr_btc_spread()
