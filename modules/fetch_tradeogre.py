import requests
from error_logger import log_to_file
from fetch_coingecko import get_coingecko_price

def get_tradeogre_price():
    url = "https://tradeogre.com/api/v1/ticker/BTC-XMR"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        print("[DEBUG] TradeOgre raw response:", data)

        # BTC per XMR (correct interpretation of TradeOgre price)
        btc_per_xmr = float(data['price'])

        # Get USD per BTC from CoinGecko
        btc_usd = get_coingecko_price()
        if btc_usd is None:
            raise ValueError("Failed to fetch BTC/USD price")

        # Convert BTC/XMR to USD/XMR
        xmr_usd = btc_per_xmr * btc_usd

        # Sanity check
        if xmr_usd < 50 or xmr_usd > 500:
            raise ValueError(f"Unrealistic TradeOgre XMR price: {xmr_usd}")

        return xmr_usd

    except Exception as e:
        log_to_file("fetch_tradeogre", f"TradeOgre fetch failed: {e}")
        print(f"[ERROR] TradeOgre fetch failed: {e}")
        return None
