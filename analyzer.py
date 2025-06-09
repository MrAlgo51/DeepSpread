# src/analyzer.py

import sqlite3
import pandas as pd

DB_PATH = "data/deepspread.db"

def compute_and_store_returns():
    print("🚨 Inside compute_and_store_returns()")  # DEBUG LINE
    print("📥 Loading signals...")
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM signals", conn)
    conn.close()

    if df.empty or "btc_price" not in df.columns:
        print("❌ signals table is empty or missing 'btc_price'")
        return

    print(f"✅ Loaded {len(df)} signals")
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    for h in [1, 2, 4]:
        df[f"return_{h}h"] = df["btc_price"].shift(-h) / df["btc_price"] - 1

    df_returns = df[["timestamp", "return_1h", "return_2h", "return_4h"]].copy()
    print(f"📊 Prepared returns with shape: {df_returns.shape}")

    try:
        conn = sqlite3.connect(DB_PATH)
        df_returns.to_sql("returns", conn, if_exists="replace", index=False)
        conn.close()
        print("✅ Stored returns into `returns` table")
    except Exception as e:
        print("❌ Failed to write to returns table:", e)

def load_merged_data():
    conn = sqlite3.connect(DB_PATH)
    df_signals = pd.read_sql_query("SELECT * FROM signals", conn)
    df_returns = pd.read_sql_query("SELECT * FROM returns", conn)
    conn.close()
    df = pd.merge(df_signals, df_returns, on="timestamp")
    return df

def analyze_score_buckets(df, return_col="return_1h"):
    df = df.copy()
    df = df[df[return_col].notnull()]
    df["score_bin"] = pd.cut(df["score"], bins=[i / 10 for i in range(11)], include_lowest=True, right=False)

    grouped = df.groupby("score_bin").agg(
        avg_return=(return_col, "mean"),
        win_rate=(return_col, lambda x: (x > 0).mean()),
        count=(return_col, "count")
    ).reset_index()

    print(f"\n=== {return_col.upper()} BY SCORE BUCKET ===")
    print(grouped.to_string(index=False))
    return grouped

def main():
    df = load_merged_data()
    analyze_score_buckets(df, "return_1h")
    analyze_score_buckets(df, "return_2h")
    analyze_score_buckets(df, "return_4h")

if __name__ == "__main__":
    import sys
    print("🧵 Args:", sys.argv)  # DEBUG LINE
    if len(sys.argv) > 1 and sys.argv[1] == "compute":
        print("🧮 Computing forward returns...")
        compute_and_store_returns()
    else:
        main()
