# modules/binance_ws.py

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import asyncio
import websockets

from config.premium_settings import MARK_PRICE_WS_URL

async def listen_to_mark_price(callback):
    """Connects to Binance WS and sends BTCUSDT mark price + funding rate to callback."""
    while True:
        try:
            async with websockets.connect(MARK_PRICE_WS_URL) as ws:
                print("[WS] Connected to Binance markPrice stream.")
                async for message in ws:
                    data = json.loads(message)
                    print(f"[WS] Raw message: {data}")  # 👈 shows every incoming WS payload

                    if data.get("s") == "BTCUSDT":
                       mark_price = float(data["p"])
                       funding_rate = float(data["r"])
                       print(f"[WS] Parsed mark: {mark_price}, funding: {funding_rate}")
                       await callback(mark_price, funding_rate)


        except Exception as e:
            print(f"[WS] Error: {e}. Reconnecting in 5 seconds...")
            await asyncio.sleep(5)
