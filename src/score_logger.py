# src/score_logger.py

import os
import sys
import sqlite3
from datetime import datetime, timezone

# --- Setup: Add /modules to sys.path ---
current_dir = os.path.dirname(os.path.abspath(__file__))                    # /DeepSpread/src
project_root = os.path.abspath(os.path.join(current_dir, ".."))            # /DeepSpread
modules_path = os.path.join(project_root, "modules")                       # /DeepSpread/modules
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

# ✅ Now safe to import from modules/
from config import DB_PATH
from error_logger import log_to_file
from sqlite_logger import log_signal
from fetch_latest import fetch_latest_usdt_premium
from scoring import compute_score

# --- Function: Get latest rows from mempool_logs and signals ---
def get_latest_rows(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch latest mempool data from mempool_logs
    cursor.execute("""
        SELECT timestamp, unconfirmed_tx, mempool_size, median_fee, low_bucket, med_bucket, high_bucket
        FROM mempool_logs
        ORDER BY timestamp DESC LIMIT 1
    """)
    mempool_row = cursor.fetchone()

    # Get latest spread entry from signals
    cursor.execute("""
        SELECT * FROM signals
        WHERE spread_pct != 0 AND median_fee = 0
        ORDER BY timestamp DESC
        LIMIT 1
    """)
    spread_row = cursor.fetchone()

    conn.close()
    return mempool_row, spread_row

# --- Main Script ---
db_path = DB_PATH
mempool_row, spread_row = get_latest_rows(db_path)

# Fetch USDT premium
usdt_row = fetch_latest_usdt_premium()
if usdt_row is None:
    print("[score_logger] Missing USDT premium data, cannot score.")
    log_to_file("score_logger", "Missing USDT premium data, cannot score.")
    sys.exit()

usdt_timestamp, btc_usd, btc_usdt, premium_pct, z_score_usdt = usdt_row

# Debug prints
print("[DEBUG] Mempool row:", mempool_row)
print("[DEBUG] Spread row:", spread_row)
print("[DEBUG] USDT Premium:", usdt_row)

if not mempool_row or not spread_row:
    print("[SKIP] Missing data, cannot score.")
    log_to_file("score_logger", "Missing data, cannot score.")
    sys.exit()

try:
    # Parse timestamps
    mem_ts = datetime.strptime(mempool_row[0], '%Y-%m-%d %H:%M:%S UTC')
    spd_ts = datetime.strptime(spread_row[0], '%Y-%m-%d %H:%M:%S UTC')
    time_diff = abs((mem_ts - spd_ts).total_seconds())

    if time_diff > 60:
        print(f"[SKIP] Timestamps too far apart ({time_diff:.1f} sec)")
        log_to_file("score_logger", f"Timestamps too far apart ({time_diff:.1f} sec)")
        sys.exit()

    # Parse values
    mem_tx_count = int(mempool_row[1])
    median_fee = float(mempool_row[3])
    spread_val = round(float(spread_row[2]), 2)
    btc_price = round(float(spread_row[1]), 2)

    # Compute score
    score = compute_score(
        median_fee=median_fee,
        unconfirmed_tx=mem_tx_count,
        spread_pct=spread_val,
        usdt_premium_z=z_score_usdt
    )

    print(f"[DEBUG] Score inputs: fee={median_fee}, txs={mem_tx_count}, spread={spread_val}, z={z_score_usdt} => score={score}")

    if score is None:
        print("[SKIP] Score is None, skipping logging.")
        log_to_file("score_logger", "Score is None, skipped.")
        sys.exit()

    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    # Log to SQLite
    log_signal(
        timestamp=timestamp,
        btc_price=btc_price,
        spread_pct=spread_val,
        median_fee=median_fee,
        unconfirmed_tx=mem_tx_count,
        score=score
    )

    print(f"[{timestamp}] Score: {score}")
    log_to_file("score_logger", f"Score: {score}")

except Exception as e:
    print(f"[ERROR] {e}")
    log_to_file("score_logger", f"Exception: {e}")
