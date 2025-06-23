import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from modules.spot_price_fetcher import fetch_spot_price
import asyncio

async def test():
    price = await fetch_spot_price()
    print(f"[TEST] Spot price: {price}")

asyncio.run(test())
