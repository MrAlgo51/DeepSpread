# src/spread_logger.py

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

from fetch_kraken import get_kraken_price             # ✅ XMR/USD
from fetch_tradeogre import get_tradeogre_price       # ✅ XMR/USD (via BTC)
from config import DB_PATH
from error_logger import log_to_file

def ensure_table_exists(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS spread (
            timestamp TEXT,
            kraken_price REAL,
            spread_pct REAL
        )
    """)

def main():
    try:
        k_price = get_kraken_price()        # ✅ XMR/USD
        t_price = get_tradeogre_price()     # ✅ XMR/USD

        if k_price is None or t_price is None:
            print("[SKIP] Missing price data, cannot compute spread.")
            return

        spread_pct = ((t_price - k_price) / k_price) * 100
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        print(f"[DEBUG] Kraken XMR/USD: {k_price}")
        print(f"[DEBUG] TradeOgre XMR/USD: {t_price}")
        print(f"[DEBUG] Spread %: {spread_pct:.5f}")

        if abs(spread_pct) > 100:
            msg = f"Unrealistic spread detected: {spread_pct:.2f}%"
            log_to_file("spread_logger", msg)
            print(f"[ERROR][SPREAD] {msg}")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        ensure_table_exists(cursor)

        cursor.execute("""
            INSERT INTO spread (timestamp, kraken_price, spread_pct)
            VALUES (?, ?, ?)
        """, (now, k_price, spread_pct))

        conn.commit()
        conn.close()

        print(f"[SPREAD] → {now}, {k_price:.1f}, {spread_pct:.4f}%")

    except Exception as e:
        log_to_file("spread_logger", str(e))
        print(f"[ERROR][SPREAD] {e}")

if __name__ == "__main__":
    main()
