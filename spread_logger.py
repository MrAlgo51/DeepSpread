import requests
import datetime
import csv
import os

def fetch_price(pair):
    url = f"https://api.kraken.com/0/public/Ticker?pair={pair}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        result = data["result"]
        key = list(result.keys())[0]
        price = float(result[key]["c"][0])
        return price
    except Exception as e:
        print(f"[ERROR] Fetching {pair} failed: {e}")
        return None

btc_price = fetch_price("XBTUSD")
xmr_price = fetch_price("XMRUSD")

if btc_price is None or xmr_price is None:
    print("[SKIPPED] Incomplete data, not logging.")
else:
    spread = btc_price / xmr_price
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    log_row = [timestamp, btc_price, xmr_price, spread]

    log_file = "spread_log.csv"
    file_exists = os.path.isfile(log_file)

    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "BTC/USD", "XMR/USD", "Spread (BTC/XMR)"])
        writer.writerow(log_row)

    print(f"[{timestamp}] BTC: ${btc_price} | XMR: ${xmr_price} | Spread: {spread:.2f}")
