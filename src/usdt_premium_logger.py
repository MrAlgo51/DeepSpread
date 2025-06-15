import os
import sys
import sqlite3
import pandas as pd
from modules.utils import get_current_utc_timestamp  # ✅ Centralized timestamp


# Setup module path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

from fetch_kraken_btcusd import get_kraken_btcusd
from fetch_coingecko_btcusd import get_coingecko_btcusd
from config import DB_PATH
from error_logger import log_to_file
from scoring import compute_z_score_from_series

def ensure_table_exists(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usdt_premium (
            timestamp TEXT,
            kraken_usd REAL,
            binance_usdt REAL,
            premium_pct REAL,
            z_score REAL
        )
    """)

def get_recent_premiums(conn, limit=20):
    try:
        df = pd.read_sql_query(
            "SELECT premium_pct FROM usdt_premium ORDER BY timestamp DESC LIMIT ?",
            conn, params=(limit,)
        )
        return df["premium_pct"][::-1]  # return Series in chronological order
    except Exception as e:
        log_to_file("usdt_premium_logger", f"Failed to read premium history: {e}")
        return pd.Series(dtype="float64")

def main():
    try:
        print("🔥 usdt_premium_logger.py is running")

        kraken_price = get_kraken_btcusd()
        binance_price = get_coingecko_btcusd()

        if kraken_price is None or binance_price is None:
            print("[SKIP] Missing price data, cannot compute premium.")
            return

        premium_pct = ((binance_price - kraken_price) / kraken_price) * 100

        if abs(premium_pct) > 20:
            log_to_file("usdt_premium_logger", f"Unrealistic premium: {premium_pct:.2f}%")
            print(f"[ERROR][PREMIUM] Unrealistic premium: {premium_pct:.2f}%")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        ensure_table_exists(cursor)

        recent_series = get_recent_premiums(conn)
        z_score = compute_z_score_from_series(recent_series, premium_pct)

        now = get_current_utc_timestamp()


        cursor.execute("""
            INSERT INTO usdt_premium (timestamp, kraken_usd, binance_usdt, premium_pct, z_score)
            VALUES (?, ?, ?, ?, ?)
        """, (now, kraken_price, binance_price, premium_pct, z_score))

        conn.commit()
        conn.close()

        print(f"[USDT_PREMIUM] → {now}, premium: {premium_pct:.4f}%, z: {z_score:.4f}")

    except Exception as e:
        log_to_file("usdt_premium_logger", f"Runtime error: {e}")
        print(f"[ERROR][USDT_PREMIUM] {e}")

if __name__ == "__main__":
    main()
