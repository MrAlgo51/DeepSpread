import os
import sys
import sqlite3

# Step 1: Set project root path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Step 2: Now imports will work
from modules.config import DB_PATH



def reset_usdt_premium_table():
    print("🔁 Resetting 'usdt_premium' table...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop the old table if it exists
    cursor.execute("DROP TABLE IF EXISTS usdt_premium")

    # Create the new table using correct columns (Bitfinex-based)
    cursor.execute("""
        CREATE TABLE usdt_premium (
            timestamp TEXT,
            btc_usd REAL,
            btc_usdt REAL,
            premium_pct REAL,
            z_score REAL
        )
    """)

    conn.commit()
    conn.close()
    print("✅ usdt_premium table has been reset successfully.")

if __name__ == "__main__":
    reset_usdt_premium_table()
