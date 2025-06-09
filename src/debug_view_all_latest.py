# src/debug_view_all_latest.py

import sqlite3
import os

# Determine database path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
db_path = os.path.join(project_root, "data", "deepspread.db")
print(f"[DEBUG] Using DB path: {db_path}")

def fetch_latest(table, cursor):
    try:
        cursor.execute(f"SELECT * FROM {table} ORDER BY timestamp DESC LIMIT 1")
        row = cursor.fetchone()
        return row
    except Exception as e:
        return f"[ERROR] Fetching from {table}: {e}"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

tables = ["mempool_logs", "spread", "usdt_premium", "signals"]

for table in tables:
    row = fetch_latest(table, cursor)
    print(f"[{table.upper()}] → {row}")

conn.close()
