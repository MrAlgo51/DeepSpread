import os
import sys
import sqlite3

# Set up path to modules/
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

from config import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
    SELECT * FROM signals
    WHERE median_fee > 0
    ORDER BY timestamp DESC
    LIMIT 5
""")

rows = cursor.fetchall()
print("\nMost recent mempool rows (median_fee > 0):")
for row in rows:
    print(row)

conn.close()
