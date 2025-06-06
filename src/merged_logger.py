import os
import sys
import requests
import sqlite3
from datetime import datetime, timezone

# Setup path to include /modules
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
modules_path = os.path.join(project_root, "modules")
if modules_path not in sys.path:
    sys.path.insert(0, modules_path)

import config
from error_logger import log_to_file
from sqlite_logger import log_signal

def fetch_spread():
    try:
        kraken_url = "https://api.kraken.com/0/public/Ticker?pair=XXMRZUSD"
        ogre_url = "https://tradeogre.com/api/v1/ticker/xmr-usdt"

        kraken_resp = requests.get(kraken_url)
        ogre_resp = requests.get(ogre_url)

        kraken_resp.raise_for_status()
        ogre_resp.raise_for_status()

        kraken_price = float(kraken_resp.json()["result"]["XXMRZUSD"]["c"][0])
        ogre_price = float(ogre_resp.json()["price"])

        spread_pct = round(((ogre_price - kraken_price) / kraken_price) * 100, 3)
        return spread_pct
    except Exception as e:
        log_to_file("merged_logger", f"ERROR fetching spread: {str(e)}")
        return None

def fetch_mempool():
    try:
        response = requests.get(config.MEMPOOL_API)
        response.raise_for_status()
        data = response.json()

        median_fee = 0
        histogram = data.get("fee_histogram", [])
        total_txs = sum(bucket[1] for bucket in histogram)
        cumulative = 0
        for fee_rate, tx_count in histogram:
            cumulative += tx_count
            if cumulative >= total_txs / 2:
                median_fee = round(fee_rate, 2)
                break

        return median_fee, data.get("count", 0)
    except Exception as e:
        log_to_file("merged_logger", f"ERROR fetching mempool: {str(e)}")
        return None, None

def fetch_btc_price():
    try:
        url = "https://api.kraken.com/0/public/Ticker?pair=XXBTZUSD"
        response = requests.get(url)
        response.raise_for_status()
        btc_price = float(response.json()["result"]["XXBTZUSD"]["c"][0])
        return btc_price
    except Exception as e:
        log_to_file("merged_logger", f"ERROR fetching BTC price: {str(e)}")
        return None

def main():
    try:
        spread_pct = fetch_spread()
        median_fee, unconfirmed_tx = fetch_mempool()
        btc_price = fetch_btc_price()

        if None in (spread_pct, median_fee, unconfirmed_tx, btc_price):
            log_to_file("merged_logger", "ERROR: Missing data, skipping log.")
            return

        # Simple scoring logic
        score = round((abs(spread_pct) + median_fee / 10 + unconfirmed_tx / 5000), 3)

        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        log_signal(timestamp, btc_price, spread_pct, median_fee, unconfirmed_tx, score)

        print(f"[{timestamp}] BTC: {btc_price}, Spread: {spread_pct}%, Fee: {median_fee}, TXs: {unconfirmed_tx}, Score: {score}")
    except Exception as e:
        log_to_file("merged_logger", f"ERROR: {str(e)}")

if __name__ == "__main__":
    main()
