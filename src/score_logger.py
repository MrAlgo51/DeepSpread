import os, sys
import sqlite3  # ✅ Required!

# Setup path to modules/
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

# ✅ Clean imports
from modules.utils import get_current_utc_timestamp
from config import DB_PATH
from scoring import compute_score
from error_logger import log_to_file


def ensure_table_exists(cursor):
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

def get_latest_rows(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, low_fee_blocks, unconfirmed_tx
        FROM mempool_logs
        ORDER BY timestamp DESC
        LIMIT 1
    """)
    mempool_row = cursor.fetchone()

    cursor.execute("""
        SELECT timestamp, spread_pct
        FROM spread
        ORDER BY timestamp DESC
        LIMIT 1
    """)
    spread_row = cursor.fetchone()

    cursor.execute("""
        SELECT timestamp, premium_pct
        FROM usdt_premium
        ORDER BY timestamp DESC
        LIMIT 1
    """)
    usdt_row = cursor.fetchone()

    conn.close()
    return mempool_row, spread_row, usdt_row

def main():
    try:
        print("🔥 score_logger.py is running")

        mempool_row, spread_row, usdt_row = get_latest_rows(DB_PATH)

        if not (mempool_row and spread_row and usdt_row):
            print("[SKIP] One or more input rows missing.")
            return

        low_fee_blocks = mempool_row[1]
        unconfirmed_tx = mempool_row[2]
        spread_pct = spread_row[1]
        premium_pct = usdt_row[1]

        score = compute_score(spread_pct, low_fee_blocks, premium_pct)
        now = get_current_utc_timestamp()

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        ensure_table_exists(cursor)

        btc_price = None
        cursor.execute("SELECT kraken_btcusd FROM spread ORDER BY timestamp DESC LIMIT 1")

        row = cursor.fetchone()
        if row and row[0] is not None:
           btc_price = row[0]
        else:
           print("[SKIP] BTC price is None. Skipping insert.")
           return
        if score is None:
           print("[SKIP] Score is None. Skipping insert.")
           return


        cursor.execute("""
            INSERT INTO signals (timestamp, btc_price, spread_pct, median_fee, unconfirmed_tx, score)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (now, btc_price, spread_pct, low_fee_blocks, unconfirmed_tx, score))

        conn.commit()
        conn.close()

        print(f"[SCORE] → {now}, score: {score:.4f}")

    except Exception as e:
        log_to_file("score_logger", f"Runtime error: {e}")
        print(f"[ERROR][SCORE_LOGGER] {e}")

if __name__ == "__main__":
    main()
