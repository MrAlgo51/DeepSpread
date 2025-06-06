import sqlite3
import config

def init_db():
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            timestamp TEXT PRIMARY KEY,
            btc_price REAL,
            spread_pct REAL,
            median_fee INTEGER,
            unconfirmed_tx INTEGER,
            score REAL
        )
    """)
    conn.commit()
    conn.close()

def log_signal(timestamp: str, btc_price: float, spread_pct: float,
               median_fee: int, unconfirmed_tx: int, score: float):
    init_db()  # ensure table exists before writing
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO signals 
        (timestamp, btc_price, spread_pct, median_fee, unconfirmed_tx, score)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (timestamp, btc_price, spread_pct, median_fee, unconfirmed_tx, score))
    conn.commit()
    conn.close()
