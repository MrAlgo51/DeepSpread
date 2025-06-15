# src/inspect_returns_table.py
import sqlite3

DB_PATH = "data/deepspread.db"

def inspect_returns_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(returns)")
    columns = cursor.fetchall()
    print("Returns table columns:")
    for col in columns:
        print(col)

    conn.close()

if __name__ == "__main__":
    inspect_returns_table()
