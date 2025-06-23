import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio
from datetime import datetime
import aiosqlite

from modules.binance_ws import listen_to_mark_price
from modules.spot_price_fetcher import fetch_spot_price
from config.premium_settings import DB_PATH, SNAPSHOT_INTERVAL

running = True
latest_mark = None
latest_funding = None

def handle_shutdown():
    global running
    running = False
    print("[MAIN] Shutdown signal received. Exiting gracefully...")

async def update_ws_data(mark_price, funding_rate):
    global latest_mark, latest_funding
    latest_mark = mark_price
    latest_funding = funding_rate

async def snapshot_loop():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS binance_premium (
                timestamp TEXT PRIMARY KEY,
                spot_price REAL NOT NULL,
                mark_price REAL NOT NULL,
                funding_rate REAL NOT NULL,
                premium_pct REAL NOT NULL
            )
        """)
        await db.commit()

        while running:
            spot = await fetch_spot_price()
            mark = latest_mark
            funding = latest_funding

            print(f"[DEBUG] spot: {spot}, mark: {mark}, funding: {funding}")

            if None in (spot, mark, funding):
                print("[LOOP] Missing data, skipping this cycle.")
            else:
                premium_pct = ((mark - spot) / spot) * 100
                timestamp = datetime.utcnow().isoformat()

                await db.execute("""
                    INSERT OR IGNORE INTO binance_premium 
                    (timestamp, spot_price, mark_price, funding_rate, premium_pct)
                    VALUES (?, ?, ?, ?, ?)
                """, (timestamp, spot, mark, funding, premium_pct))

                await db.commit()
                print(f"[LOGGED] {timestamp} | Spot: {spot:.2f} | Mark: {mark:.2f} | Premium: {premium_pct:.4f}%")

            await asyncio.sleep(SNAPSHOT_INTERVAL)

def try_setup_signal_handlers():
    import signal
    try:
        loop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, handle_shutdown)
    except (NotImplementedError, RuntimeError):
        print("[MAIN] Signal handlers not supported or event loop not ready — skipping.")


async def main():
    try_setup_signal_handlers()
    await asyncio.gather(
        listen_to_mark_price(update_ws_data),
        snapshot_loop()
    )
print(f"[DEBUG] DB_PATH = {DB_PATH}")


if __name__ == "__main__":
    asyncio.run(main())
