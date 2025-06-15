# src/reset_signals_table.py

import sqlite3

DB_PATH = "data/deepspread.db"

def reset_signals_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Drop and recreate the signals table with 6 columns
    cursor.execute("DROP TABLE IF EXISTS signals")
    cursor.execute("""
        CREATE TABLE signals (
            timestamp TEXT,
            btc_price REAL,
            spread_pct REAL,
            median_fee REAL,
            unconfirmed_tx INTEGER,
            score REAL
        )
    """)

    conn.commit()
    conn.close()
    print("✅ signals table reset successfully (no z_score).")

if __name__ == "__main__":
    reset_signals_table()
