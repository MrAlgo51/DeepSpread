# modules/fetch_latest.py

import sqlite3
from config import DB_PATH, USDT_PREMIUM_TABLE
from error_logger import log_to_file

def fetch_latest_usdt_premium():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT timestamp, btc_usd, btc_usdt, premium_pct, z_score
            FROM {USDT_PREMIUM_TABLE}
            ORDER BY timestamp DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        conn.close()
        return row
    except Exception as e:
        log_to_file("fetch_latest", f"Error fetching latest USDT premium: {str(e)}")
        return None
