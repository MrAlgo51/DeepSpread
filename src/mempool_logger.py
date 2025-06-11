import sys
import os
import requests
import sqlite3
from datetime import datetime, timezone  # ✅ timezone-aware

# ✅ Add project root to sys.path so modules can be imported cleanly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.path_setup import fix_paths
fix_paths()

from modules.config import DB_PATH


def fetch_mempool_data():
    url = "https://mempool.space/api/v1/fees/mempool-blocks"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract congestion data
        low = sum(1 for b in data if b["medianFee"] <= 2)
        med = sum(1 for b in data if 2 < b["medianFee"] <= 10)
        high = sum(1 for b in data if b["medianFee"] > 10)

        return {
            "low": low,
            "med": med,
            "high": high
        }
    except Exception as e:
        print(f"[mempool_logger] Failed to fetch mempool data: {e}")
        return None


def log_mempool_data():
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    mempool = fetch_mempool_data()

    if mempool is None:
        print("[mempool_logger] ❌ No mempool data. Skipping.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mempool (
                timestamp TEXT PRIMARY KEY,
                low_fee_blocks INTEGER,
                med_fee_blocks INTEGER,
                high_fee_blocks INTEGER
            )
        """)
        cursor.execute("""
            INSERT OR REPLACE INTO mempool (
                timestamp, low_fee_blocks, med_fee_blocks, high_fee_blocks
            ) VALUES (?, ?, ?, ?)
        """, (timestamp, mempool["low"], mempool["med"], mempool["high"]))
        conn.commit()
        conn.close()

        print(f"[mempool_logger] Logged mempool data @ {timestamp}")
        print(f"[mempool_logger] low={mempool['low']} | med={mempool['med']} | high={mempool['high']}")
    except Exception as e:
        print(f"[mempool_logger] ❌ DB write failed: {e}")


if __name__ == "__main__":
    log_mempool_data()
