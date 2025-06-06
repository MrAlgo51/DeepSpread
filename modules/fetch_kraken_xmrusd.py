# modules/fetch_kraken_xmrusd.py

import requests
from modules import config

def get_kraken_xmrusd():
    try:
        response = requests.get(config.KRAKEN_XMRUSD_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        price = float(data['result']['XXMRZUSD']['c'][0])
        return price
    except Exception as e:
        print(f"[ERROR] Kraken XMR/USD fetch failed: {e}")
        return None
