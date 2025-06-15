import sqlite3

# Connect to your DeepSpread database
conn = sqlite3.connect("data/deepspread.db")
cursor = conn.cursor()

# Ask SQLite to describe the 'signals' table
cursor.execute("PRAGMA table_info(signals);")
columns = cursor.fetchall()

# Print out the columns it finds
print("Signals table columns:")
for col in columns:
    print(col)

conn.close()
