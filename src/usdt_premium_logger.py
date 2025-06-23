import os
import sys
import sqlite3
import pandas as pd

# Set up project root for module imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from modules.utils import get_current_utc_timestamp
from modules.fetch_bitfinex_usdt_premium import get_bitfinex_usdt_premium
from modules.error_logger import log_to_file
from modules.scoring import compute_z_score_from_series
from modules.config import DB_PATH


def ensure_table_exists(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usdt_premium (
            timestamp TEXT,
            btc_usd REAL,
            btc_usdt REAL,
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

        btc_usd, btc_usdt, premium_pct = get_bitfinex_usdt_premium()

        if btc_usd is None or btc_usdt is None:
            print("[SKIP] Missing Bitfinex data.")
            return

        if abs(premium_pct) > 20:
            log_to_file("usdt_premium_logger", f"Unrealistic premium: {premium_pct:.2f}%")
            print(f"[ERROR][PREMIUM] Unrealistic premium: {premium_pct:.2f}%")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        ensure_table_exists(cursor)

        now = get_current_utc_timestamp()

        recent_series = get_recent_premiums(conn)
        if len(recent_series) < 5:
            z_score = 0.0
        else:
            z_score = compute_z_score_from_series(recent_series, premium_pct)

        cursor.execute("""
            INSERT INTO usdt_premium (timestamp, btc_usd, btc_usdt, premium_pct, z_score)
            VALUES (?, ?, ?, ?, ?)
        """, (now, btc_usd, btc_usdt, premium_pct, z_score))

        conn.commit()
        conn.close()

        z_display = f"{z_score:.4f}" if z_score is not None else "N/A"
        print(f"[USDT_PREMIUM] → {now}, premium: {premium_pct:.4f}%, z: {z_display}")

    except Exception as e:
        log_to_file("usdt_premium_logger", f"Runtime error: {e}")
        print(f"[ERROR][USDT_PREMIUM] {e}")


if __name__ == "__main__":
    main()
