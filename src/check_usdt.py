import os
import sys
import sqlite3

# ✅ Add /modules to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

from config import DB_PATH

def show_latest_usdt_premium(n=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM usdt_premium
        ORDER BY timestamp DESC
        LIMIT ?
    """, (n,))
    rows = cursor.fetchall()
    conn.close()

    print(f"\nLatest {n} entries in usdt_premium:\n")
    for row in rows:
        print(row)

if __name__ == "__main__":
    show_latest_usdt_premium()
