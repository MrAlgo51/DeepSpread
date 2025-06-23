import os, sys
import requests
import sqlite3

# Setup module path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

from utils import get_current_utc_timestamp
from config import DB_PATH
from error_logger import log_to_file

def ensure_table_exists(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mempool_logs (
            timestamp TEXT,
            median_fee REAL,
            mempool_size REAL,
            unconfirmed_tx INTEGER
        )
    """)

def fetch_mempool_data():
    try:
        response = requests.get("https://mempool.space/api/v1/fees/recommended", timeout=10)
        response.raise_for_status()
        fees = response.json()

        response2 = requests.get("https://mempool.space/api/mempool", timeout=10)
        response2.raise_for_status()
        mempool = response2.json()

        median_fee = fees["halfHourFee"]
        unconfirmed_tx = mempool["count"]
        mempool_size = mempool["vsize"]

        return median_fee, mempool_size, unconfirmed_tx

    except Exception as e:
        log_to_file("mempool_logger", f"Fetch error: {e}")
        return None

def main():
    try:
        print("🔥 mempool_logger.py is running")

        data = fetch_mempool_data()
        if data is None:
            print("[SKIP] No mempool data fetched.")
            return

        median_fee, mempool_size, unconfirmed_tx = data
        now = get_current_utc_timestamp()

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        ensure_table_exists(cursor)

        cursor.execute("""
            INSERT INTO mempool_logs (
                timestamp, median_fee, mempool_size, unconfirmed_tx
            ) VALUES (?, ?, ?, ?)
        """, (now, median_fee, mempool_size, unconfirmed_tx))

        conn.commit()
        conn.close()

        print(f"[MEMPOOL] → {now}, fee: {median_fee}, txs: {unconfirmed_tx}")

    except Exception as e:
        log_to_file("mempool_logger", f"Runtime error: {e}")
        print(f"[ERROR][MEMPOOL_LOGGER] {e}")

if __name__ == "__main__":
    main()
