# dslog.py
import requests
import csv
import os
from datetime import datetime, timezone

def fetch_kraken_price():
    try:
        url = "https://api.kraken.com/0/public/Ticker?pair=XXMRXXBT"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        price = float(data['result']['XXMRXXBT']['c'][0])
        return price
    except Exception as e:
        print(f"[KRAKEN ERROR] {e}")
        return None

def fetch_tradeogre_price():
    try:
        url = "https://tradeogre.com/api/v1/ticker/BTC-XMR"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        price = float(data['price'])
        return price
    except Exception as e:
        print(f"[OGRE ERROR] {e}")
        return None

def calculate_spread(kraken_price, ogre_price):
    if kraken_price is None or ogre_price is None:
        return None
    try:
        spread = (ogre_price - kraken_price) / kraken_price * 100
        return spread
    except ZeroDivisionError:
        return None

def append_to_csv(timestamp, kraken, ogre, spread):
    log_path = os.path.join("logs", "spread_log.csv")
    file_exists = os.path.isfile(log_path)

    with open(log_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["timestamp", "kraken_price", "ogre_price", "spread_pct"])
        writer.writerow([timestamp, kraken, ogre, spread])

def main():
    kraken = fetch_kraken_price()
    ogre = fetch_tradeogre_price()
    spread = calculate_spread(kraken, ogre)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z")

    if spread is not None:
        print(f"[{now}] Spread: {spread:.4f}% | Kraken: {kraken:.6f} | Ogre: {ogre:.6f}")
        append_to_csv(now, kraken, ogre, spread)
    else:
        print(f"[{now}] Error calculating spread.")

if __name__ == "__main__":
    main()
