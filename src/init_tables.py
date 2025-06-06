import config
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import sqlite3
from modules.config import DB_PATH

conn = sqlite3.connect(config.DB_PATH)
cursor = conn.cursor()

# Create mempool table
cursor.execute("""
CREATE TABLE IF NOT EXISTS mempool (
    timestamp TEXT PRIMARY KEY,
    median_fee REAL,
    unconfirmed_tx INTEGER,
    mempool_size INTEGER,
    low_fee_bucket INTEGER,
    med_fee_bucket INTEGER,
    high_fee_bucket INTEGER
)
""")
print("✅ mempool table created (or already exists)")

# Create spread table
cursor.execute("""
CREATE TABLE IF NOT EXISTS spread (
    timestamp TEXT PRIMARY KEY,
    spread_pct REAL,
    spread_zscore REAL,
    divergence REAL
)
""")
print("✅ spread table created (or already exists)")

# Create usdt_premium table
cursor.execute("""
CREATE TABLE IF NOT EXISTS usdt_premium (
    timestamp TEXT PRIMARY KEY,
    btc_price REAL,
    usdt_premium_pct REAL,
    usdt_zscore REAL
)
""")
print("✅ usdt_premium table created (or already exists)")

# Create signals table
cursor.execute("""
CREATE TABLE IF NOT EXISTS signals (
    timestamp TEXT PRIMARY KEY,
    btc_price REAL,
    spread_pct REAL,
    median_fee REAL,
    unconfirmed_tx INTEGER,
    score REAL
)
""")
print("✅ signals table created (or already exists)")

conn.commit()
conn.close()
