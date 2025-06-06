import requests

def get_tradeogre_price():
    url = "https://tradeogre.com/api/v1/ticker/BTC-XMR"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        price = float(data['price'])
        return price
    except Exception as e:
        print(f"[ERROR] TradeOgre fetch failed: {e}")
        return None
