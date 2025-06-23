import requests
import pandas as pd
from datetime import datetime, timedelta
import argparse

KRAKEN_OHLC_URL = "https://api.kraken.com/0/public/OHLC"


def fetch_kraken_ohlcv(pair="XXBTZUSD", interval=1, start_time=None, end_time=None):
    """
    Fetches 1m OHLCV data from Kraken between start_time and end_time.
    """
    if start_time is None:
        start_time = datetime.utcnow() - timedelta(hours=4)
    if end_time is None:
        end_time = datetime.utcnow()

    since = int(start_time.timestamp())
    end_ts = int(end_time.timestamp())

    ohlcv_data = []

    while since < end_ts:
        params = {
            "pair": pair,
            "interval": interval,
            "since": since
        }
        resp = requests.get(KRAKEN_OHLC_URL, params=params)
        data = resp.json()

        result_key = list(data['result'].keys())[0]
        candles = data['result'][result_key]
        if not candles:
            break

        df = pd.DataFrame(candles, columns=[
            "timestamp", "open", "high", "low", "close", "vwap", "volume", "count"
        ])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit='s')
        ohlcv_data.append(df)

        since = int(candles[-1][0]) + 60  # move to next minute

    full_df = pd.concat(ohlcv_data, ignore_index=True) if ohlcv_data else pd.DataFrame()
    return full_df


def main():
    parser = argparse.ArgumentParser(description="Fetch Kraken OHLCV data and compute VWAP.")
    parser.add_argument("--start", type=str, required=True, help="Start time in ISO format (e.g. 2025-06-20T00:00:00Z)")
    parser.add_argument("--end", type=str, required=True, help="End time in ISO format (e.g. 2025-06-20T08:00:00Z)")
    args = parser.parse_args()

    start_time = datetime.fromisoformat(args.start.replace("Z", ""))
    end_time = datetime.fromisoformat(args.end.replace("Z", ""))

    df = fetch_kraken_ohlcv(start_time=start_time, end_time=end_time)

    if df.empty:
        print("No data returned.")
        return

    df["vwap_calc"] = (df["close"].astype(float) * df["volume"].astype(float)).cumsum() / df["volume"].astype(float).cumsum()
    df.to_csv("vwap_output.csv", index=False)
    print("VWAP data saved to vwap_output.csv")


if __name__ == "__main__":
    main()
