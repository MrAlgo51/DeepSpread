# src/create_all_tables.py

import os
import sys
import sqlite3

# Setup for module imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from modules import config

def create_signals_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            timestamp TEXT PRIMARY KEY,
            btc_price REAL,
            spread_pct REAL,
            median_fee REAL,
            unconfirmed_tx INTEGER,
            score REAL
        )
    """)

def create_returns_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS returns (
            timestamp TEXT PRIMARY KEY,
            score REAL,
            fwd_return_1h REAL,
            fwd_return_2h REAL,
            fwd_return_4h REAL
        )
    """)

def create_usdt_premium_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usdt_premium (
            timestamp TEXT PRIMARY KEY,
            btc_usd REAL,
            btc_usdt REAL,
            premium_pct REAL,
            z_score REAL
        )
    """)

if __name__ == "__main__":
    conn = sqlite3.connect(config.DB_PATH)
    create_signals_table(conn)
    create_returns_table(conn)
    create_usdt_premium_table(conn)
    conn.commit()
    conn.close()
    print("[INIT] All tables created or already exist.")
