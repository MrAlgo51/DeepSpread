import os
import sys
import sqlite3
import pandas as pd
from datetime import datetime, timezone

# Setup module path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

from fetch_kraken_spread import get_kraken_spread_pct
from fetch_tradeogre_xmrbtc import get_tradeogre_xmrbtc
from scoring import compute_z_score_from_series
from config import DB_PATH
from error_logger import log_to_file
from utils import get_current_utc_timestamp
from fetchers import get_kraken_btcusd


def ensure_table_exists(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS spread (
            timestamp TEXT,
            kraken_spread REAL,
            tradeogre_spread REAL,
            spread_pct REAL,
            z_score REAL,
            kraken_btcusd REAL
        )
    """)


def get_recent_spreads(conn, limit=20):
    try:
        df = pd.read_sql_query(
            "SELECT spread_pct FROM spread ORDER BY timestamp DESC LIMIT ?",
            conn, params=(limit,)
        )
        return df["spread_pct"][::-1]  # chronological order
    except Exception as e:
        log_to_file("spread_logger", f"Failed to read spread history: {e}")
        return pd.Series(dtype="float64")


def main():
    try:
        now = get_current_utc_timestamp()
        print("🔥 spread_logger.py is running")

        kraken = get_kraken_spread_pct()
        kraken_btcusd = get_kraken_btcusd()

        if kraken_btcusd is None:
            print("[SKIP] Missing BTC/USD price.")
            return

        tradeogre = get_tradeogre_xmrbtc()
        if kraken is None or tradeogre is None:
            print("[SKIP] Missing spread data, cannot compute.")
            return

        spread_pct = (kraken - tradeogre) / tradeogre * 100
        if abs(spread_pct) > 100:
            log_to_file("spread_logger", f"Unrealistic spread: {spread_pct:.2f}%")
            print(f"[ERROR][SPREAD] Unrealistic spread: {spread_pct:.2f}%")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        ensure_table_exists(cursor)

        recent_series = get_recent_spreads(conn)
        recent_list = list(recent_series)
        recent_list.append(spread_pct)
        z_score = compute_z_score_from_series(pd.Series(recent_list), recent_list[-1], window=20)

        cursor.execute("""
            INSERT INTO spread (timestamp, kraken_spread, tradeogre_spread, spread_pct, z_score, kraken_btcusd)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (now, kraken, tradeogre, spread_pct, z_score, kraken_btcusd))

        conn.commit()
        conn.close()

        print(f"[SPREAD] → {now}, spread: {spread_pct:.4f}%, z: {z_score:.4f}")

    except Exception as e:
        log_to_file("spread_logger", f"Runtime error: {e}")
        print(f"[ERROR][SPREAD_LOGGER] {e}")


if __name__ == "__main__":
    main()
