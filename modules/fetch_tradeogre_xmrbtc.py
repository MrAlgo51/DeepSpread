# modules/fetch_tradeogre_xmrbtc.py

import requests

def get_tradeogre_xmrbtc():
    try:
        url = "https://tradeogre.com/api/v1/ticker/BTC-XMR"
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print(f"[ERROR] Failed to fetch TradeOgre XMR/BTC: {e}")
        return None
