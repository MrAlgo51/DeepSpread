# src/reset_derived_tables.py
import sqlite3

conn = sqlite3.connect("data/deepspread.db")
cursor = conn.cursor()
cursor.execute("DELETE FROM signals")
cursor.execute("DELETE FROM returns")
conn.commit()
conn.close()
print("✅ Cleared signals and returns tables.")
