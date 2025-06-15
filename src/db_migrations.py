import sqlite3
import os
import sys

# Setup path for modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

from config import DB_PATH

def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return column in [row[1] for row in cursor.fetchall()]

def add_column_if_missing(cursor, table, column, col_type):
    if not column_exists(cursor, table, column):
        print(f"🔧 Adding missing column '{column}' to '{table}'...")
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")

def ensure_table_and_columns(conn):
    cursor = conn.cursor()

    # mempool_logs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mempool_logs (
            timestamp TEXT,
            median_fee REAL,
            mempool_size REAL,
            low_fee_blocks INTEGER,
            unconfirmed_tx INTEGER
        )
    """)
    add_column_if_missing(cursor, "mempool_logs", "low_fee_blocks", "INTEGER")

    # spread
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS spread (
            timestamp TEXT,
            kraken_btc_usd REAL,
            kraken_xmr_usd REAL,
            kraken_spread REAL,
            spread_pct REAL,
            spread_z REAL
        )
    """)

    # usdt_premium
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usdt_premium (
            timestamp TEXT,
            binance_price REAL,
            coingecko_price REAL,
            premium_pct REAL,
            premium_z REAL
        )
    """)

    # signals
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            timestamp TEXT,
            btc_price REAL,
            spread_pct REAL,
            median_fee REAL,
            unconfirmed_tx INTEGER,
            score REAL
        )
    """)

    conn.commit()

def main():
    print("🧠 Running DB schema migration check...")
    conn = sqlite3.connect(DB_PATH)
    ensure_table_and_columns(conn)
    conn.close()
    print("✅ DB schema check complete.")

if __name__ == "__main__":
    main()
