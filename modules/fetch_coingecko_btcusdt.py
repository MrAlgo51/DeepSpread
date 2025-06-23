# modules/fetch_coingecko_btcusdt.py
import requests

def get_coingecko_btcusdt():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()["bitcoin"]["usd"]  # <— FIXED
    except Exception as e:
        print(f"[ERROR][COINGECKO BTCUSDT] {e}")
        return None
