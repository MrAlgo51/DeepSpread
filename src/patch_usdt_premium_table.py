import os
import sys
import sqlite3

# Add /modules to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

import config

# Connect and patch
conn = sqlite3.connect(config.DB_PATH)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE usdt_premium ADD COLUMN z_score REAL")
    print("[PATCH] z_score column added to usdt_premium table.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("[PATCH] z_score column already exists.")
    else:
        raise

conn.commit()
conn.close()
