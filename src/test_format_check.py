import sqlite3

conn = sqlite3.connect("data/deepspread.db")
cursor = conn.cursor()

cursor.execute("SELECT timestamp FROM signals ORDER BY timestamp DESC LIMIT 3")
rows = cursor.fetchall()
for row in rows:
    print(f"[CHECK] timestamp = {row[0]}")
conn.close()
