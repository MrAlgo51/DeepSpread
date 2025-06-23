# src/xmr_usd_premium_logger.py
import os
import sys
import sqlite3
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from modules.fetch_coingecko_xmrbtc import get_coingecko_xmrbtc
from modules.fetch_coingecko_btcusdt import get_coingecko_btcusdt
from modules.fetch_kraken_xmrusd import get_kraken_xmrusd
from modules.config import DB_PATH
from modules.utils import get_current_utc_timestamp
from modules.error_logger import log_to_file
from modules.scoring import compute_z_score_from_series

def ensure_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS xmr_usd_premium (
            timestamp TEXT,
            kraken_usd REAL,
            binance_implied_usd REAL,
            premium_pct REAL,
            z_score REAL
        )
    """)

def get_recent_premiums(conn, limit=20):
    try:
        df = pd.read_sql_query(
            "SELECT premium_pct FROM xmr_usd_premium ORDER BY timestamp DESC LIMIT ?",
            conn, params=(limit,)
        )
        return df["premium_pct"][::-1]
    except Exception as e:
        log_to_file("xmr_usd_premium_logger", f"Failed to read premium history: {e}")
        return pd.Series(dtype="float64")

def main():
    try:
        print("🔥 xmr_usd_premium_logger.py is running")

        xmr_btc = get_coingecko_xmrbtc()
        btc_usdt = get_coingecko_btcusdt()
        kraken_usd = get_kraken_xmrusd()

        if None in (xmr_btc, btc_usdt, kraken_usd):
            print("[SKIP] Missing pricing data.")
            return

        binance_implied = xmr_btc * btc_usdt
        premium_pct = (kraken_usd - binance_implied) / binance_implied * 100

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        ensure_table(cursor)

        recent_series = get_recent_premiums(conn)
        z_score = 0.0 if len(recent_series) < 5 else compute_z_score_from_series(recent_series, premium_pct)

        now = get_current_utc_timestamp()
        cursor.execute("""
            INSERT INTO xmr_usd_premium (timestamp, kraken_usd, binance_implied_usd, premium_pct, z_score)
            VALUES (?, ?, ?, ?, ?)
        """, (now, kraken_usd, binance_implied, premium_pct, z_score))

        conn.commit()
        conn.close()

        z_display = f"{z_score:.4f}" if z_score is not None else "N/A"
        print(f"[XMR_USD_PREMIUM] → {now}, premium: {premium_pct:.4f}%, z: {z_display}")

    except Exception as e:
        log_to_file("xmr_usd_premium_logger", f"Runtime error: {e}")
        print(f"[ERROR][XMR_USD_PREMIUM] {e}")

if __name__ == "__main__":
    main()
