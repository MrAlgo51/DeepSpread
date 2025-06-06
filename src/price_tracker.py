
# src/price_tracker.py

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)
import sqlite3
from datetime import datetime, timezone, timedelta

# Setup module path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

import config
from error_logger import log_to_file

def parse_timestamp(ts_str):
    return datetime.strptime(ts_str, '%Y-%m-%d %H:%M:%S UTC').replace(tzinfo=timezone.utc)

try:
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM signals ORDER BY timestamp DESC LIMIT 1")
    latest = cursor.fetchone()

    if not latest:
        raise ValueError("No signal data found.")

    ts_str, btc_price, *_ = latest
    signal_time = parse_timestamp(ts_str)

    now = datetime.now(timezone.utc)
    horizons = {
    '1m': timedelta(minutes=1),
    '3m': timedelta(minutes=3),
    '5m': timedelta(minutes=5)
}


    for label, delta in horizons.items():
        target_time = signal_time + delta
        # TEMPORARY for testing
        if True:

            cursor.execute(f"""
                SELECT * FROM usdt_premium
                WHERE timestamp >= ?
                ORDER BY timestamp ASC
                LIMIT 1
            """, (target_time.strftime('%Y-%m-%d %H:%M:%S UTC'),))
            result = cursor.fetchone()
            if result:
                future_ts, future_price, *_ = result
                forward_return = (future_price - btc_price) / btc_price
                cursor.execute("""
                    INSERT INTO forward_returns (timestamp, horizon, forward_return)
                    VALUES (?, ?, ?)
                """, (ts_str, label, forward_return))
                print(f"[{label}] Forward return: {round(forward_return * 100, 2)}%")

    conn.commit()
    conn.close()

except Exception as e:
    log_to_file("price_tracker", f"Error: {str(e)}")
    print(f"❌ Error: {e}")
