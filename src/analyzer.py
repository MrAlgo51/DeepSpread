# src/analyzer.py

import sqlite3
import pandas as pd
import numpy as np

DB_PATH = "data/deepspread.db"

def load_merged_data():
    conn = sqlite3.connect(DB_PATH)
    df_signals = pd.read_sql_query("SELECT * FROM signals", conn)
    df_returns = pd.read_sql_query("SELECT * FROM returns", conn)
    conn.close()

    df_signals['timestamp'] = pd.to_datetime(df_signals['timestamp'])
    df_returns['timestamp'] = pd.to_datetime(df_returns['timestamp'])

    # Only keep return columns that aren't already in signals
    return_cols = [col for col in df_returns.columns if col not in df_signals.columns or col == 'timestamp']
    df = pd.merge(df_signals, df_returns[return_cols], on="timestamp")

    return df


def generate_forward_return_table():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM signals ORDER BY timestamp ASC", conn)
    conn.close()

    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    df.set_index('timestamp', inplace=True)

    # For testing: Only return_1h
    for hours in [1]:
        df[f'return_{hours}h'] = df['btc_price'].shift(-hours) / df['btc_price'] - 1

    columns = ['btc_price', 'spread_pct', 'median_fee', 'unconfirmed_tx', 'z_score', 'score', 'return_1h']
    returns_df = df[columns].dropna(subset=['return_1h'])

    print(f"📉 Original rows: {len(df)}")
    print(f"✅ Rows with complete forward returns: {len(returns_df)}")

    conn = sqlite3.connect(DB_PATH)
    returns_df.to_sql("returns", conn, if_exists="replace", index_label="timestamp")
    conn.close()

    print("✅ Forward return table generated.")

def analyze_implied_xmr_btc_spread():
    conn = sqlite3.connect(DB_PATH)
    df_spread = pd.read_sql_query("SELECT timestamp, kraken_price FROM spread", conn)
    df_signals = pd.read_sql_query("SELECT timestamp, btc_price FROM signals", conn)
    conn.close()

    df_spread['timestamp'] = pd.to_datetime(df_spread['timestamp'], utc=True)
    df_signals['timestamp'] = pd.to_datetime(df_signals['timestamp'], utc=True)

    df = pd.merge_asof(
        df_spread.sort_values('timestamp'),
        df_signals.sort_values('timestamp'),
        on='timestamp',
        direction='nearest',
        tolerance=pd.Timedelta('5min')
    )

    df.dropna(inplace=True)
    df['implied_xmr_btc'] = df['kraken_price'] / df['btc_price']
    df['zscore'] = (df['implied_xmr_btc'] - df['implied_xmr_btc'].rolling(24).mean()) / df['implied_xmr_btc'].rolling(24).std()

    conn = sqlite3.connect(DB_PATH)
    df[['timestamp', 'implied_xmr_btc', 'zscore']].to_sql("implied_spread", conn, if_exists="replace", index=False)
    conn.close()
    print("✅ Implied BTC/XMR spread reconstructed and written to SQLite.")

def analyze_score_buckets(df, return_col="return_1h"):
    df = df.copy()
    df = df[df["btc_price"] > 0]
    df = df[df["score"].notnull()]
    df = df[df[return_col].notnull()]

    print(f"\nAnalyzing {len(df)} valid signals for {return_col}")
    df["score_bin"] = pd.cut(df["score"], bins=[i / 10 for i in range(11)], include_lowest=True, right=False)
    grouped = df.groupby("score_bin", observed=False).agg(
        avg_return=(return_col, "mean"),
        win_rate=(return_col, lambda x: (x > 0).mean()),
        count=(return_col, "count")
    ).reset_index()

    grouped = grouped.sort_values("score_bin")
    print(f"\n=== {return_col.upper()} BY SCORE BUCKET ===")
    print(grouped.to_string(index=False))

def find_optimal_thresholds(df, return_col="return_1h"):
    print(f"\n=== OPTIMAL SCORE THRESHOLDS for {return_col.upper()} ===")
    df = df.copy()
    df = df[df["btc_price"] > 0]
    df = df[df[return_col].notnull()]

    results = []
    for threshold in np.arange(0.1, 1.0, 0.1):
        filtered = df[df["score"] > threshold]
        if len(filtered) == 0:
            continue
        avg_return = filtered[return_col].mean()
        win_rate = (filtered[return_col] > 0).mean()
        count = len(filtered)
        results.append((round(threshold, 1), avg_return, win_rate, count))

    results_df = pd.DataFrame(results, columns=["Threshold", "Avg Return", "Win Rate", "Count"])
    results_df = results_df.sort_values(by="Avg Return", ascending=False)
    print(results_df.to_string(index=False))

def main():
    generate_forward_return_table()
    analyze_implied_xmr_btc_spread()

    df = load_merged_data()
    print(f"\n📊 Merged dataset rows: {len(df)}")
    print(df.head())

    for col in ["return_1h"]:
        analyze_score_buckets(df, col)
        find_optimal_thresholds(df, col)

if __name__ == "__main__":
    main()
