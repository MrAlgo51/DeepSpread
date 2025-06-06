# modules/fetch_kraken.py

import requests
from modules import config

def get_kraken_price():
    try:
        response = requests.get("https://api.kraken.com/0/public/Ticker?pair=XXBTZUSD", timeout=10)
        response.raise_for_status()
        data = response.json()
        price = float(data['result']['XXBTZUSD']['c'][0])
        return price
    except Exception as e:
        print(f"[ERROR] Kraken BTC/USD fetch failed: {e}")
        return None
