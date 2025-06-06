# src/create_usdt_premium_table.py

import os
import sys

# Fix import path so modules/config can be loaded
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from modules import config
import sqlite3

conn = sqlite3.connect(config.DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usdt_premium (
    timestamp TEXT PRIMARY KEY,
    btc_usdt REAL,
    btc_usd REAL,
    premium_pct REAL,
    zscore REAL
)
""")

conn.commit()
conn.close()

print("[INIT] usdt_premium table created or already exists.")
