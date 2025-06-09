import requests
import sqlite3
from datetime import datetime
from modules.config import DB_PATH

def fetch_mempool_data():
    try:
        # Get basic mempool stats
        r1 = requests.get("https://mempool.space/api/mempool", timeout=10)
        r1.raise_for_status()
        mempool_stats = r1.json()

        # Get recommended fee estimates
        r2 = requests.get("https://mempool.space/api/v1/fees/recommended", timeout=10)
        r2.raise_for_status()
        fee_estimates = r2.json()

        return {
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "unconfirmed_tx": mempool_stats.get("count", 0),
            "mempool_size": mempool_stats.get("vsize", 0),
            "median_fee": fee_estimates.get("halfHourFee", 0)  # ✅ renamed for consistency
        }

    except Exception as e:
        print(f"❌ Error fetching mempool data: {e}")
        return None

def log_mempool_data():
    data = fetch_mempool_data()
    if not data:
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ✅ Unified column naming: median_fee
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mempool_logs (
            timestamp TEXT PRIMARY KEY,
            unconfirmed_tx INTEGER,
            mempool_size INTEGER,
            median_fee REAL
        )
    """)

    cursor.execute("""
        INSERT OR IGNORE INTO mempool_logs (
            timestamp,
            unconfirmed_tx,
            mempool_size,
            median_fee
        ) VALUES (?, ?, ?, ?)
    """, (
        data["timestamp"],
        data["unconfirmed_tx"],
        data["mempool_size"],  # ✅ fix from data["vsize"]
        data["median_fee"]
    ))

    conn.commit()
    conn.close()
    print(f"✅ Logged mempool data @ {data['timestamp']}")

if __name__ == "__main__":
    log_mempool_data()
