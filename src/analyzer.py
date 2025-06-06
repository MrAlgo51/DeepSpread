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

    df = pd.merge(df_signals, df_returns, on="timestamp")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def analyze_score_buckets(df, return_col="return_1h"):
    df = df.copy()
    df = df[df["price_now"] > 0]
    df = df[df["score"].notnull()]
    df = df[df[return_col].notnull()]

    # Optional: Enable this to focus on "congested" mempool environments
    # df = df[df["median_fee"] > 5]

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

    # Optional: Save results to CSV for external analysis
    grouped.to_csv(f"data/score_analysis_{return_col}.csv", index=False)

def main():
    df = load_merged_data()
    for col in ["return_1h", "return_2h", "return_4h"]:
        print(f"\nAnalyzing {df[df[col].notnull()].shape[0]} valid signals for {col}")
        analyze_score_buckets(df, col)
        find_optimal_thresholds(df, col)


def find_optimal_thresholds(df, return_col="return_1h"):
    print(f"\n=== OPTIMAL SCORE THRESHOLDS for {return_col.upper()} ===")
    df = df.copy()
    df = df[df["price_now"] > 0]
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

if __name__ == "__main__":
    main()
