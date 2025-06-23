import os
import sys
import asyncio
import aiosqlite
from datetime import datetime, timezone

# Set up module paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

from config import DB_PATH
from fetchers import get_kraken_btcusd
from error_logger import log_to_file
from scoring import score_signal

async def get_latest_funding_rate(conn):
    async with conn.execute("""
        SELECT funding_rate FROM binance_premium
        WHERE funding_rate IS NOT NULL
        ORDER BY timestamp DESC
        LIMIT 1
    """) as cursor:
        row = await cursor.fetchone()
        return row[0] if row else None

async def get_funding_rate_with_retry(conn, retries=6, delay=5):
    for attempt in range(retries):
        rate = await get_latest_funding_rate(conn)
        if rate is not None:
            return rate
        print(f"[WAIT] No funding rate yet — retrying ({attempt + 1}/6) in {delay}s...")
        await asyncio.sleep(delay)
    return None

async def log_signal():
    try:
        timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        btc_usd = get_kraken_btcusd()
        print("[DEBUG] BTC price:", btc_usd)

        async with aiosqlite.connect(DB_PATH) as conn:
            funding_rate = await get_funding_rate_with_retry(conn)

            if None in (btc_usd, funding_rate):
                print("[MERGED LOGGER] Missing data — skipping.")
                return

            score = score_signal(
                funding_rate=funding_rate,
                median_fee=0,
                unconfirmed_tx=0,
                spread_pct=0,
                spread_delta=0
            )

            await conn.execute("""
                CREATE TABLE IF NOT EXISTS signals (
                    timestamp TEXT PRIMARY KEY,
                    btc_price REAL,
                    spread_pct REAL,
                    spread_delta REAL,
                    median_fee REAL,
                    unconfirmed_tx INTEGER,
                    score REAL,
                    funding_rate REAL
                )
            """)

            await conn.execute("""
                INSERT OR REPLACE INTO signals (
                    timestamp, btc_price, spread_pct, spread_delta,
                    median_fee, unconfirmed_tx, score, funding_rate
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                timestamp, btc_usd, 0.0, 0.0, 0.0, 0, score, funding_rate
            ))

            await conn.commit()
            print(f"[MERGED LOGGER] → {timestamp} | Score: {score:.4f} | Funding: {funding_rate:.6f}")

    except Exception as e:
        log_to_file("merged_logger", str(e))
        print(f"[ERROR][MERGED LOGGER] {e}")

if __name__ == "__main__":
    asyncio.run(log_signal())
