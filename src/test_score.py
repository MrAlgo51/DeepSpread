import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.scoring import compute_score

test_cases = [
    # median_fee, unconfirmed_tx, spread_pct, usdt_premium_z
    (30, 250000, 0.6, 1.5),
    (55, 400000, 1.2, 2.0),
    (5, 10000, 0.2, -0.5),
    (None, 250000, 0.6, 1.5),
    (30, None, 0.6, 1.5),
    (30, 250000, None, 1.5),
    (30, 250000, 0.6, None),
    (80, 600000, 2.5, 4.0),
]

print("Testing compute_score...\n")
for i, (fee, txs, spread, z) in enumerate(test_cases, 1):
    score = compute_score(fee, txs, spread, z)
    print(f"Test {i}: fee={fee}, txs={txs}, spread={spread}, z={z} => score = {score}")
