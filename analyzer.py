import sqlite3
import pandas as pd

DB_PATH = "data/deepspread.db"

def load_merged_data():
    conn = sqlite3.connect(DB_PATH)
    df_signals = pd.read_sql_query("SELECT * FROM signals", conn)
    df_returns = pd.read_sql_query("SELECT * FROM returns", conn)
    conn.close()
    df = pd.merge(df_signals, df_returns, on="timestamp")
    return df

def analyze_score_buckets(df, return_col="return_1h"):
    """
    Group signals by score buckets and compute average return and win rate.
    """
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

if __name__ == "__main__":
    df = load_merged_data()
    analyze_score_buckets(df, return_col="return_1h")
