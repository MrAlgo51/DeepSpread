import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)
from datetime import datetime, timezone
import sqlite3

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules import config
from modules.error_logger import log_to_file
from modules.sqlite_logger import log_signal
from modules.fetch_kraken import get_kraken_price
from modules.fetch_tradeogre import get_tradeogre_price
from modules.fetch_kraken_xmrusd import get_kraken_xmrusd

def ensure_table_exists(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS spread (
            timestamp TEXT,
            kraken_price REAL,
            tradeogre_price REAL,
            spread_pct REAL,
            spread_z REAL,
            kraken_xmr_usd REAL,
            tradeogre_xmr_usd REAL
        )
    """)

# Fetch prices
btc_usd = get_kraken_price()
xmr_btc = get_tradeogre_price()
xmr_usd_kraken = get_kraken_xmrusd()

if None in (btc_usd, xmr_btc, xmr_usd_kraken):
    print("[SKIP] Missing price data")
    log_to_file("spread_logger", "Missing price data")
else:
    try:
        xmr_usd_tradeogre = btc_usd * xmr_btc
        spread_pct = (xmr_usd_tradeogre - xmr_usd_kraken) / xmr_usd_kraken * 100
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

        print(f"[{timestamp}] Kraken: ${xmr_usd_kraken:.2f}, TradeOgre: ${xmr_usd_tradeogre:.2f}, Spread: {spread_pct:.2f}%")
        log_to_file("spread_logger", f"Kraken: {xmr_usd_kraken}, TradeOgre: {xmr_usd_tradeogre}, Spread: {round(spread_pct, 2)}%")

        # Save to spread table
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        ensure_table_exists(cursor)

        cursor.execute("""
            INSERT INTO spread (
                timestamp,
                kraken_price,
                tradeogre_price,
                spread_pct,
                spread_z,
                kraken_xmr_usd,
                tradeogre_xmr_usd
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            timestamp,
            xmr_usd_kraken,
            xmr_usd_tradeogre,
            round(spread_pct, 4),
            0.0,  # placeholder for spread_z
            xmr_usd_kraken,
            xmr_usd_tradeogre
        ))

        conn.commit()
        conn.close()

        # Log to signals table
        log_signal(
            timestamp=timestamp,
            btc_price=btc_usd,
            spread_pct=round(spread_pct, 4),
            median_fee=0,
            unconfirmed_tx=0,
            score=0.0
        )

    except Exception as e:
        print(f"[ERROR] {e}")
        log_to_file("spread_logger", f"Exception: {e}")
