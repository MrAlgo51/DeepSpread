# modules/fetch_binance_btcusdt.py
import requests

def get_binance_btcusdt():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
        response = requests.get(url)
        response.raise_for_status()
        return float(response.json()["price"])
    except Exception as e:
        print(f"[ERROR][BINANCE BTCUSDT] {e}")
        return None