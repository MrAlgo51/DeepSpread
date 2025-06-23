# modules/spot_price_fetcher.py

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import aiohttp
from config.premium_settings import SPOT_REST_URL

async def fetch_spot_price():
    print("[DEBUG] fetch_spot_price() was called")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(SPOT_REST_URL) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    print(f"[DEBUG] Raw Bitfinex response: {data}")
                    return float(data[6])  # LAST_PRICE
                else:
                    print(f"[REST] Non-200 response: {resp.status}")
    except Exception as e:
        print(f"[REST] Error fetching spot price: {e}")

    return None
