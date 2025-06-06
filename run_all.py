# run_all.py

import subprocess

scripts = [
    "spread_logger.py",
    "mempool_logger.py",
    "usdt_premium_logger.py",
    "score_logger.py"
]

for script in scripts:
    print(f"\n--- Running {script} ---")
    subprocess.run(["python", f"src/{script}"])
