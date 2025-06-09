# modules/fetch_coingecko_btcusd.py

import requests
from error_logger import log_to_file

def get_coingecko_btcusd():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        price = float(data['bitcoin']['usd'])
        print("[DEBUG] CoinGecko BTC price:", price)

        if price < 1000 or price > 200000:
            raise ValueError(f"Unrealistic BTC price from CoinGecko: {price}")

        return price

    except Exception as e:
        log_to_file("fetch_coingecko_btcusd", f"CoinGecko fetch failed: {e}")
        print(f"[ERROR] CoinGecko fetch failed: {e}")
        return None
