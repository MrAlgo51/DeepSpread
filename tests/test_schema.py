import config
import sqlite3
import os
from modules.config import DB_PATH

def check_schema(table_name, expected_cols):
conn = sqlite3.connect(config.DB_PATH)
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table_name})")
    cols = [row[1] for row in cur.fetchall()]
    conn.close()

    missing = [c for c in expected_cols if c not in cols]
    if missing:
        print(f"[FAIL] {table_name}: missing {missing}")
    else:
        print(f"[PASS] {table_name}: all good")

if __name__ == "__main__":
    check_schema("mempool", [
        "timestamp", "median_fee", "unconfirmed_tx", "mempool_size",
        "low_fee_bucket", "med_fee_bucket", "high_fee_bucket"
    ])
    check_schema("usdt_premium", [
        "timestamp", "btc_usd", "btc_usdt", "premium_pct", "z_score"
    ])
    check_schema("spread", [
        "timestamp", "kraken_xmr_usd", "tradeogre_xmr_usd", "spread_pct", "spread_zscore"
    ])
