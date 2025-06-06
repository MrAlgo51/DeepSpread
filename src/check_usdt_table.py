import os
import config
# src/check_usdt_table.py

import sys, os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import sqlite3
from modules.config import DB_PATH

conn = sqlite3.connect(config.DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT * FROM usdt_premium ORDER BY timestamp DESC LIMIT 5")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
