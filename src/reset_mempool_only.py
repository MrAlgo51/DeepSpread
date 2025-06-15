# src/reset_mempool_only.py
import sqlite3
conn = sqlite3.connect("data/deepspread.db")
cursor = conn.cursor()
cursor.execute("DELETE FROM mempool_logs")
conn.commit()
conn.close()
print("✅ Cleared mempool_logs table.")
