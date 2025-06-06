import sqlite3

conn = sqlite3.connect("data/deepspread.db")
cursor = conn.cursor()

# Drop old table if exists
cursor.execute("DROP TABLE IF EXISTS returns")

# Create with correct schema
cursor.execute("""
CREATE TABLE returns (
    timestamp TEXT PRIMARY KEY,
    price_now REAL,
    return_1h REAL,
    return_2h REAL,
    return_4h REAL,
    score REAL
)
""")

conn.commit()
conn.close()
print("[fix_returns_table] ✅ Table reset complete.")
