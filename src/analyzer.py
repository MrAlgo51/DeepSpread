# src/analyzer.py

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

DB_PATH = "data/deepspread.db"


def generate_forward_return_table():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query("SELECT timestamp, btc_price FROM signals", conn)
    print(f"[DEBUG] Loaded {len(df)} rows from signals")

    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    df = df.sort_values("timestamp").reset_index(drop=True)

    for h in [1, 2, 4]:
        df[f"fwd_return_{h}h"] = (df["btc_price"].shift(-h) - df["btc_price"]) / df["btc_price"] * 100

    print(f"[DEBUG] Rows before dropna: {len(df)}")
    df.dropna(inplace=True)
    print(f"[DEBUG] Rows after dropna: {len(df)}")

    df_out = df[["timestamp", "fwd_return_1h", "fwd_return_2h", "fwd_return_4h"]]
    df_out.to_sql("returns", conn, if_exists="replace", index=False)

    conn.close()
    print("[analyzer] Forward returns table created.")


def analyze_score_buckets(bucket_width=0.1):
    conn = sqlite3.connect(DB_PATH)

    # Load signal + return data
    signals = pd.read_sql_query("SELECT timestamp, score FROM signals", conn)
    returns = pd.read_sql_query("SELECT timestamp, fwd_return_1h FROM returns", conn)
    conn.close()

    # Convert timestamps to datetime
    signals["timestamp"] = pd.to_datetime(signals["timestamp"])
    returns["timestamp"] = pd.to_datetime(returns["timestamp"])

    # Sort for asof merge
    signals = signals.sort_values("timestamp")
    returns = returns.sort_values("timestamp")

    # Merge using nearest timestamp
    df = pd.merge_asof(signals, returns, on="timestamp", direction="nearest", tolerance=pd.Timedelta("5min"))

    # Drop any rows that still didn't match
    df.dropna(subset=["fwd_return_1h"], inplace=True)

    # Bucket scores
    df["score_bucket"] = (df["score"] // bucket_width) * bucket_width
    df["score_bucket"] = df["score_bucket"].round(2)

    # Group and analyze
    grouped = df.groupby("score_bucket")["fwd_return_1h"]
    summary = pd.DataFrame({
        "avg_return": grouped.mean(),
        "win_rate": (grouped.apply(lambda x: (x > 0).mean()) * 100).round(2),
        "count": grouped.count()
    }).reset_index()

    print("\n[analyzer] Score Bucket Analysis (1h forward return):")
    print(summary)
    return summary



def analyze_implied_xmr_btc_spread():
    print("[analyzer] (stub) analyze_implied_xmr_btc_spread() not implemented yet.")

if __name__ == "__main__":
    generate_forward_return_table()
