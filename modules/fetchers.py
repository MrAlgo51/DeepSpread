# modules/fetchers.py

import requests

def get_kraken_btcusd():
    url = "https://api.kraken.com/0/public/Ticker?pair=XBTUSD"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data["result"]["XXBTZUSD"]["c"][0])  # Last trade closed price
    except Exception as e:
        print(f"[ERROR][FETCHER] Failed to fetch BTC/USD from Kraken: {e}")
        return None
