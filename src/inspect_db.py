# src/inspect_db.py
import os
import sys

# Set project root and append to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from modules import config

import sqlite3


conn = sqlite3.connect(config.DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in DB:")
for table in tables:
    print("-", table[0])

conn.close()
