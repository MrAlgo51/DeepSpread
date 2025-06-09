import requests

def get_kraken_price():
    try:
        url = "https://api.kraken.com/0/public/Ticker?pair=XMRUSD"
        response = requests.get(url, timeout=10)
        data = response.json()
        return float(data["result"]["XXMRZUSD"]["c"][0])
    except Exception as e:
        print(f"[ERROR][fetch_kraken] {e}")
        return None
