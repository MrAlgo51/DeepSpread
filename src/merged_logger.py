import os
import sys
import sqlite3
import requests
from datetime import datetime, timezone

# Setup module path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

from config import DB_PATH
from error_logger import log_to_file

MEMPOOL_API = "https://mempool.space/api/mempool"

def fetch_mempool_data():
    response = requests.get(MEMPOOL_API)
    response.raise_for_status()
    data = response.json()
    return {
        "unconfirmed_tx": data["count"],
        "mempool_size": data["vsize"],
        "median_fee": data["feeMedian"],
        "low_fee_bucket": data.get("vsize10", 0),
        "med_fee_bucket": data.get("vsize50", 0),
        "high_fee_bucket": data.get("vsize90", 0),
    }

def ensure_table_exists(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mempool (
            timestamp TEXT,
            median_fee REAL,
            unconfirmed_tx INTEGER,
            mempool_size INTEGER,
            low_fee_bucket INTEGER,
            med_fee_bucket INTEGER,
            high_fee_bucket INTEGER
        )
    """)

def main():
    try:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        data = fetch_mempool_data()

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        ensure_table_exists(cursor)

        cursor.execute("""
            INSERT INTO mempool (timestamp, median_fee, unconfirmed_tx, mempool_size,
                                 low_fee_bucket, med_fee_bucket, high_fee_bucket)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            now,
            data["median_fee"],
            data["unconfirmed_tx"],
            data["mempool_size"],
            data["low_fee_bucket"],
            data["med_fee_bucket"],
            data["high_fee_bucket"]
        ))

        conn.commit()
        conn.close()
        print(f"[MEMPOOL] → {now}, {data}")

    except Exception as e:
        log_to_file("mempool_logger", str(e))
        print(f"[ERROR][MEMPOOL] {e}")

if __name__ == "__main__":
    main()
