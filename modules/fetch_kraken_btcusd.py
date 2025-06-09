# modules/fetch_kraken_btcusd.py

import requests

def get_kraken_btcusd():
    try:
        url = "https://api.kraken.com/0/public/Ticker?pair=XXBTZUSD"
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data["result"]["XXBTZUSD"]["c"][0])
    except Exception as e:
        print(f"[ERROR][fetch_kraken_btcusd] {e}")
        return None
