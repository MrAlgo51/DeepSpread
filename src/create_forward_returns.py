import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)
import sqlite3

# Setup module path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

import config

try:
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forward_returns (
            entry_timestamp TEXT,
            future_timestamp TEXT,
            price_entry REAL,
            price_future REAL,
            return_pct REAL,
            horizon TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ forward_returns table created successfully.")

except Exception as e:
    print(f"❌ Error creating table: {str(e)}")
