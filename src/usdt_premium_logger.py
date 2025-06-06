# src/usdt_premium_logger.py

import os
import sys
import requests
import sqlite3
from datetime import datetime, timezone

# Add /modules to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

# Now do imports
import config
from error_logger import log_to_file


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


def fetch_usdt_premium():
    resp_usd = requests.get("https://api.kraken.com/0/public/Ticker?pair=XBTUSD")
    resp_usdt = requests.get("https://api.kraken.com/0/public/Ticker?pair=XBTUSDT")
    resp_usd.raise_for_status()
    resp_usdt.raise_for_status()

    price_usd = float(resp_usd.json()["result"]["XXBTZUSD"]["c"][0])
    price_usdt = float(resp_usdt.json()["result"]["XBTUSDT"]["c"][0])
    premium_pct = round(((price_usdt - price_usd) / price_usd) * 100, 3)

    # Calculate z-score using last 100 entries
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT premium_pct FROM usdt_premium ORDER BY timestamp DESC LIMIT 100")
    rows = cursor.fetchall()
    conn.close()

    premiums = [row[0] for row in rows]
    mean = sum(premiums) / len(premiums) if premiums else 0
    std = (sum((x - mean) ** 2 for x in premiums) / len(premiums)) ** 0.5 if premiums else 1
    z_score = round((premium_pct - mean) / std, 3) if std else 0

    return price_usd, price_usdt, premium_pct, z_score


def main():
    try:
        btc_usd, btc_usdt, premium_pct, z_score = fetch_usdt_premium()
        print(f"Fetched values: {btc_usd} {btc_usdt} {premium_pct} {z_score}")

        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        ensure_table_exists(cursor)

        cursor.execute("""
            INSERT INTO usdt_premium (timestamp, btc_usd, btc_usdt, premium_pct, z_score)
            VALUES (?, ?, ?, ?, ?)
        """, (timestamp, btc_usd, btc_usdt, premium_pct, z_score))

        conn.commit()
        conn.close()

        print(f"[{timestamp}] BTC/USD: {btc_usd}, BTC/USDT: {btc_usdt}, Premium: {premium_pct}%, Z-score: {z_score}")
    except Exception as e:
        log_to_file("usdt_premium", f"ERROR: {str(e)}")
        print(f"[ERROR] Failed to log USDT premium: {e}")


if __name__ == "__main__":
    main()
