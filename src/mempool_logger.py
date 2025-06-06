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

# Safe imports
import config
from error_logger import log_to_file

DB_PATH = os.path.join(project_root, "data", "deepspread.db")

def fetch_mempool_data():
    response = requests.get(config.MEMPOOL_API)
    response.raise_for_status()
    return response.json()

def calculate_median_fee(histogram):
    total_txs = sum(bucket[1] for bucket in histogram)
    cumulative = 0
    for fee_rate, tx_count in histogram:
        cumulative += tx_count
        if cumulative >= total_txs / 2:
            return round(fee_rate, 2)
    return 0.0

def calculate_fee_buckets(histogram):
    low, med, high = 0, 0, 0
    for fee_rate, tx_count in histogram:
        if fee_rate < 10:
            low += tx_count
        elif 10 <= fee_rate < 50:
            med += tx_count
        else:
            high += tx_count
    return low, med, high

def log_mempool_row(timestamp, unconfirmed_tx, mempool_size, median_fee, low, med, high):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mempool_logs (
                timestamp TEXT PRIMARY KEY,
                unconfirmed_tx INTEGER,
                mempool_size INTEGER,
                median_fee REAL,
                low_bucket INTEGER,
                med_bucket INTEGER,
                high_bucket INTEGER
            );
        """)

        cursor.execute("""
            INSERT OR REPLACE INTO mempool_logs (
                timestamp, unconfirmed_tx, mempool_size, median_fee,
                low_bucket, med_bucket, high_bucket
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (timestamp, unconfirmed_tx, mempool_size, median_fee, low, med, high))

        conn.commit()
        conn.close()

    except Exception as e:
        log_to_file("mempool_logger", f"ERROR writing to mempool_logs: {str(e)}")
        print(f"[ERROR] Failed to write to mempool_logs: {e}")

def main():
    try:
        data = fetch_mempool_data()

        tx_count = data.get("count", 0)
        mempool_size = data.get("vsize", 0)
        histogram = data.get("fee_histogram", [])

        median_fee = calculate_median_fee(histogram) if histogram else 0.0
        low, med, high = calculate_fee_buckets(histogram) if histogram else (0, 0, 0)
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

        log_mempool_row(timestamp, tx_count, mempool_size, median_fee, low, med, high)

        print(f"[{timestamp}] Mempool logged | TXs: {tx_count}, Size: {mempool_size}, Median Fee: {median_fee} | Buckets: L={low}, M={med}, H={high}")
        log_to_file("mempool_logger", f"TXs: {tx_count}, Size: {mempool_size}, Median Fee: {median_fee}, Buckets: {low}/{med}/{high}")

    except Exception as e:
        log_to_file("mempool_logger", f"ERROR fetching mempool data: {str(e)}")
        print(f"[ERROR] Failed to log mempool data: {e}")

if __name__ == "__main__":
    main()
