# src/score_logger.py

import sys
import os
import sqlite3
from datetime import datetime, timezone

# ✅ Add project root to sys.path so modules can be imported cleanly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.path_setup import fix_paths
fix_paths()

from modules.config import DB_PATH
from modules.fetch_kraken_btcusd import get_kraken_btcusd
from modules.scoring import compute_score
from modules.error_logger import log_to_file


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
        SELECT timestamp, kraken_spread, tradeogre_spread, spread_pct
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

    if not mempool_row:
        print("[score_logger] ❌ Missing mempool data — skipping.")
        return
    if not spread_row:
        print("[score_logger] ❌ Missing spread data — skipping.")
        return
    if not usdt_row:
        print("[score_logger] ❌ Missing USDT premium data — skipping.")
        return

    try:
        fee = mempool_row[3]
        unconfirmed_tx = mempool_row[1]
        spread_pct = spread_row[3]
        spread_z = None  # not logged yet
        usdt_z = usdt_row[4]

        btc_price = get_kraken_btcusd()
        score = compute_score(fee, unconfirmed_tx, spread_z, usdt_z)

        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        print(f"[DEBUG] Score inputs: fee={fee}, txs={unconfirmed_tx}, spread_z=None, usdt_z={round(usdt_z, 2)} => score={score:.4f}")

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
        """, (now, btc_price, spread_pct, fee, unconfirmed_tx, usdt_z, score))

        conn.commit()
        conn.close()
        print(f"[{now}] Score: {score:.4f}")

    except Exception as e:
        log_to_file("score_logger", str(e))
        print(f"[ERROR][score_logger] {e}")



if __name__ == "__main__":
    main()
