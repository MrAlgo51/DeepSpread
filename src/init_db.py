# src/init_db.py

import sqlite3
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules import config

# Connect to database
db_path = os.path.join(os.path.dirname(__file__), '..', 'deepspread.db')
conn = sqlite3.connect(config.DB_PATH)
cursor = conn.cursor()

# Create signals table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS signals (
    timestamp TEXT,
    btc_price REAL,
    spread_pct REAL,
    median_fee INTEGER,
    unconfirmed_tx INTEGER,
    score REAL
)
""")

conn.commit()
conn.close()
print("[INIT] signals table created or already exists.")
