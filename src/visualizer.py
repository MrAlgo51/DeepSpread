import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Config fallback
config = type("Config", (), {})()
config.DB_PATH = "data/deepspread.db"
save_dir = "charts"
os.makedirs(save_dir, exist_ok=True)


def load_data():
    conn = sqlite3.connect(config.DB_PATH)
    df = pd.read_sql_query("SELECT * FROM signals WHERE score IS NOT NULL", conn)
    conn.close()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df


def plot_score_histogram():
    df = load_data()
    plt.figure(figsize=(10, 6))
    sns.histplot(df['score'], bins=30, kde=True)
    plt.title("Distribution of Scores")
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/score_histogram.png")
    plt.show()


def plot_score_vs_median_fee():
    df = load_data()
    df = df[df['median_fee'] > 0]  # Optional filter to remove flat noise
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="score", y="median_fee", data=df)
    plt.title("Score vs Median Fee")
    plt.xlabel("Score")
    plt.ylabel("Median Fee (sats/vByte)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/score_vs_median_fee.png")
    plt.show()


def plot_score_vs_spread():
    df = load_data()
    df = df[df['spread_pct'] > 0]  # Optional filter to reduce scatter noise
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="score", y="spread_pct", data=df)
    plt.title("Score vs BTC/XMR Spread %")
    plt.xlabel("Score")
    plt.ylabel("Spread %")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/score_vs_spread.png")
    plt.show()


def plot_score_vs_return_scatter():
    conn = sqlite3.connect(config.DB_PATH)
    query = """
        SELECT s.score, r.return_1h
        FROM returns r
        JOIN signals s ON r.timestamp = s.timestamp
        WHERE r.return_1h IS NOT NULL AND s.score IS NOT NULL
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        print("[plot_score_vs_return_scatter] No return data to plot.")
        return

    plt.figure(figsize=(10, 6))
    plt.scatter(df['score'], df['return_1h'], alpha=0.6, edgecolors='k')
    plt.axhline(0, color='gray', linestyle='--', linewidth=1)
    plt.title("Score vs. Forward Return (1h)")
    plt.xlabel("Signal Score")
    plt.ylabel("1h Forward Return (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/score_vs_return_scatter.png")
    plt.show()


def plot_score_vs_forward_return(return_col="return_1h"):
    conn = sqlite3.connect(config.DB_PATH)
    query = f"""
        SELECT r.timestamp, r.{return_col}, s.score
        FROM returns r
        JOIN signals s ON r.timestamp = s.timestamp
        WHERE r.{return_col} IS NOT NULL AND s.score IS NOT NULL
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    if df.empty:
        print(f"[plot_score_vs_forward_return] No data to plot for {return_col}.")
        return

    df['score_bin'] = pd.cut(df['score'], bins=[i / 10 for i in range(0, 11)], include_lowest=True, right=False)
    grouped = df.groupby('score_bin', observed=False)[return_col].mean().reset_index()

    plt.figure(figsize=(12, 6))
    sns.barplot(x='score_bin', y=return_col, data=grouped)
    plt.title(f"Average {return_col.replace('_', ' ')} by Score Bucket")
    plt.xlabel("Score Bucket")
    plt.ylabel(f"Avg {return_col.replace('_', ' ')} (%)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/score_vs_{return_col}.png")
    plt.show()


if __name__ == "__main__":
    plot_score_histogram()
    plot_score_vs_median_fee()
    plot_score_vs_spread()
    plot_score_vs_return_scatter()
    plot_score_vs_forward_return("return_1h")
    plot_score_vs_forward_return("return_2h")
    plot_score_vs_forward_return("return_4h")
