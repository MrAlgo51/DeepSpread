# modules/fetch_kraken_xmrusd.py
import requests

def get_kraken_xmrusd():
    try:
        url = "https://api.kraken.com/0/public/Ticker?pair=XXMRZUSD"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()["result"]
        pair = list(data.keys())[0]
        return float(data[pair]["c"][0])  # last price
    except Exception as e:
        print(f"[ERROR][KRAKEN XMRUSD] {e}")
        return None