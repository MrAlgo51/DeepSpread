import os
import sys
import sqlite3
from datetime import datetime, timezone

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

def compute_z_score(premiums):
    if len(premiums) < 20:
        return 0.0  # Not enough data for meaningful z-score
    mean = sum(premiums) / len(premiums)
    stddev = (sum((x - mean) ** 2 for x in premiums) / len(premiums)) ** 0.5
    return (premiums[-1] - mean) / stddev if stddev > 0 else 0.0

def get_recent_premiums():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT premium_pct FROM usdt_premium ORDER BY timestamp DESC LIMIT 50")
        rows = cursor.fetchall()
        return [row[0] for row in reversed(rows)]  # reverse to chronological order
    except Exception as e:
        log_to_file("usdt_premium_logger", f"Failed to read history: {e}")
        return []
    finally:
        conn.close()

def main():
    try:
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

        premiums = get_recent_premiums() + [premium_pct]
        z_score = compute_z_score(premiums)

        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        ensure_table_exists(cursor)

        cursor.execute("""
            INSERT INTO usdt_premium (timestamp, kraken_usd, binance_usdt, premium_pct, z_score)
            VALUES (?, ?, ?, ?, ?)
        """, (now, kraken_price, binance_price, premium_pct, z_score))

        conn.commit()
        conn.close()

        print(f"[USDT_PREMIUM] → {now}, {kraken_price}, {binance_price}, {premium_pct:.4f}%")

    except Exception as e:
        log_to_file("usdt_premium_logger", f"Runtime error: {e}")
        print(f"[ERROR][USDT_PREMIUM] {e}")

if __name__ == "__main__":
    main()
