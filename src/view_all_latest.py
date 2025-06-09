import sys
import os

# Ensure 'modules' folder is on the import path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))

import config
print("[DEBUG] VIEWER using DB path:", config.DB_PATH)
import sqlite3

conn = sqlite3.connect(config.DB_PATH)
cursor = conn.cursor()

tables = ["mempool_logs", "spread", "usdt_premium"]
for table in tables:
    try:
        cursor.execute(f"SELECT * FROM {table} ORDER BY timestamp DESC LIMIT 1")
        row = cursor.fetchone()
        print(f"[{table.upper()}] → {row}")
    except Exception as e:
        print(f"[{table.upper()}] → ERROR: {e}")

conn.close()
