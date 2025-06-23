import requests

def get_bitfinex_usdt_premium():
    try:
        url = "https://api-pub.bitfinex.com/v2/tickers?symbols=tBTCUSD,tBTCUST"
        response = requests.get(url)
        data = response.json()

        prices = {}
        for ticker in data:
            symbol = ticker[0]  # "tBTCUSD" or "tBTCUST"
            last_price = ticker[7]
            prices[symbol] = last_price

        btc_usd = prices.get("tBTCUSD")
        btc_usdt = prices.get("tBTCUST")

        if btc_usd is None or btc_usdt is None:
            raise ValueError("Missing BTC/USD or BTC/USDT from Bitfinex response")

        premium_pct = (btc_usdt - btc_usd) / btc_usd * 100
        return btc_usd, btc_usdt, premium_pct

    except Exception as e:
        print(f"[ERROR][BITFINEX] Failed to fetch premium: {e}")
        return None, None, None
