# modules/fetch_kraken_spread.py

import requests
from error_logger import log_to_file

def get_kraken_spread_pct():
    try:
        xmr_usd_resp = requests.get("https://api.kraken.com/0/public/Ticker?pair=XMRUSD").json()
        btc_usd_resp = requests.get("https://api.kraken.com/0/public/Ticker?pair=BTCUSD").json()

        xmr_usd = float(xmr_usd_resp["result"]["XXMRZUSD"]["c"][0])
        btc_usd = float(btc_usd_resp["result"]["XXBTZUSD"]["c"][0])

        xmr_btc = xmr_usd / btc_usd  # Synthetic XMR/BTC
        return xmr_btc

    except Exception as e:
        log_to_file("fetch_kraken_spread", f"Failed to fetch Kraken prices: {e}")
        return None
