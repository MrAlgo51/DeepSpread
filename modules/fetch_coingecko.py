# modules/fetch_coingecko.py

import requests
from error_logger import log_to_file

def get_coingecko_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data["bitcoin"]["usd"])
    except Exception as e:
        log_to_file("fetch_coingecko", f"CoinGecko fetch failed: {e}")
        print(f"[ERROR] CoinGecko fetch failed: {e}")
        return None
