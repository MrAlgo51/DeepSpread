# modules/fetch_coingecko_xmrbtc.py
import requests

def get_coingecko_xmrbtc():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=monero&vs_currencies=btc"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["monero"]["btc"]
    except Exception as e:
        print(f"[ERROR][COINGECKO XMRBTC] {e}")
        return None
