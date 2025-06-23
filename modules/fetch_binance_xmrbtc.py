# modules/fetch_binance_xmrbtc.py
import requests

def get_binance_xmrbtc():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=XMRBTC"
        response = requests.get(url)
        response.raise_for_status()
        return float(response.json()["price"])
    except Exception as e:
        print(f"[ERROR][BINANCE XMRBTC] {e}")
        return None