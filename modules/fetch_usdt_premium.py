# modules/fetch_usdt_premium.py

import requests
import statistics
from modules.error_logger import log_to_file

history = []

def fetch_usdt_premium():
    try:
        # Fetch BTC/USD from Kraken
        kraken_resp = requests.get("https://api.kraken.com/0/public/Ticker?pair=XBTUSD", timeout=10).json()
        btc_usd = float(kraken_resp["result"]["XXBTZUSD"]["c"][0])

        # Fetch BTC/USDT from Coinbase
        coinbase_resp = requests.get("https://api.exchange.coinbase.com/products/BTC-USDT/ticker", timeout=10).json()
        if "price" not in coinbase_resp:
            raise ValueError(f"Coinbase price missing | Response: {coinbase_resp}")
        btc_usdt = float(coinbase_resp["price"])

        # Calculate premium
        premium_pct = round(((btc_usdt - btc_usd) / btc_usd) * 100, 3)

        # Maintain rolling history for z-score
        history.append(premium_pct)
        if len(history) > 100:
            history.pop(0)

        if len(history) > 10:
            mean = statistics.mean(history)
            stdev = statistics.stdev(history)
            z_score = round((premium_pct - mean) / stdev, 3) if stdev else 0.0
        else:
            z_score = 0.0

        return btc_usd, btc_usdt, premium_pct, z_score

    except Exception as e:
        log_to_file("usdt_premium", f"Fetch error: {str(e)}")
        return None, None, None, None
