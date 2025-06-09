# score_logger.py

import os
import sys
import sqlite3
from datetime import datetime, timezone
from modules.config import DB_PATH

# Setup module path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

from fetch_kraken_btcusd import get_kraken_btcusd  # ✅ Correct fetcher
from scoring import compute_score
from error_logger import log_to_file

def get_latest_rows(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, unconfirmed_tx, mempool_size, median_fee
        FROM mempool_logs
        ORDER BY timestamp DESC
        LIMIT 1
    """)
    mempool_row = cursor.fetchone()

    cursor.execute("""
        SELECT timestamp, kraken_price, spread_pct
        FROM spread
        ORDER BY timestamp DESC
        LIMIT 1
    """)
    spread_row = cursor.fetchone()

    cursor.execute("""
    SELECT timestamp, kraken_usd, binance_usdt, premium_pct, z_score
    FROM usdt_premium
    ORDER BY timestamp DESC
    LIMIT 1
""")

    usdt_row = cursor.fetchone()

    conn.close()
    return mempool_row, spread_row, usdt_row

def main():
    mempool_row, spread_row, usdt_row = get_latest_rows(DB_PATH)

    print(f"[DEBUG] Mempool row: {mempool_row}")
    print(f"[DEBUG] Spread row: {spread_row}")
    print(f"[DEBUG] USDT Premium: {usdt_row}")

    if not all([mempool_row, spread_row, usdt_row]):
        print("[score_logger] Missing data, cannot score.")
        return

    # Time validation (omitted here, keep if needed)

    try:
        fee = mempool_row[3]
        unconfirmed_tx = mempool_row[1]
        spread_pct = spread_row[2]
        z_score = usdt_row[4]

        btc_price = get_kraken_btcusd()  # ✅ This is now the actual BTC/USD price

        score = compute_score(fee, unconfirmed_tx, spread_pct, z_score)

        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        print(f"[DEBUG] Score inputs: fee={fee}, txs={unconfirmed_tx}, spread={spread_pct:.2f}, z={z_score} => score={score:.4f}")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                timestamp TEXT,
                btc_price REAL,
                spread_pct REAL,
                median_fee REAL,
                unconfirmed_tx INTEGER,
                z_score REAL,
                score REAL
            )
        """)

        cursor.execute("""
            INSERT INTO signals (
                timestamp, btc_price, spread_pct, median_fee, unconfirmed_tx, z_score, score
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (now, btc_price, spread_pct, fee, unconfirmed_tx, z_score, score))

        conn.commit()
        conn.close()
        print(f"[{now}] Score: {score:.4f}")

    except Exception as e:
        log_to_file("score_logger", str(e))
        print(f"[ERROR][score_logger] {e}")

if __name__ == "__main__":
    main()
