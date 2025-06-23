# src/visualizer.py

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

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


def load_merged_signals_returns():
    conn = sqlite3.connect(config.DB_PATH)
    df_signals = pd.read_sql_query("SELECT timestamp, score FROM signals", conn)
    df_returns = pd.read_sql_query("SELECT timestamp, fwd_return_1h, fwd_return_2h, fwd_return_4h FROM returns", conn)
    conn.close()

    df_signals["timestamp"] = pd.to_datetime(df_signals["timestamp"])
    df_returns["timestamp"] = pd.to_datetime(df_returns["timestamp"])

    df_signals.sort_values("timestamp", inplace=True)
    df_returns.sort_values("timestamp", inplace=True)

    merged = pd.merge_asof(df_signals, df_returns, on="timestamp", direction="nearest", tolerance=pd.Timedelta("5min"))
    merged.dropna(subset=["score"], inplace=True)
    return merged


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
    df = df[df['median_fee'] > 0]
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
    df = df[df['spread_pct'] > 0]
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
    df = load_merged_signals_returns()
    if df.empty:
        print("[plot_score_vs_return_scatter] No return data to plot.")
        return
    plt.figure(figsize=(10, 6))
    plt.scatter(df['score'], df['fwd_return_1h'], alpha=0.6, edgecolors='k')
    plt.axhline(0, color='gray', linestyle='--', linewidth=1)
    plt.title("Score vs. Forward Return (1h)")
    plt.xlabel("Signal Score")
    plt.ylabel("1h Forward Return (%)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/score_vs_return_scatter.png")
    plt.show()


def plot_score_vs_forward_return(return_col="fwd_return_1h"):
    df = load_merged_signals_returns()
    if df.empty or return_col not in df.columns:
        print(f"[plot_score_vs_forward_return] No data to plot for {return_col}.")
        return
    df = df.dropna(subset=[return_col])
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


def plot_btc_price_with_signals():
    df = load_data()
    plt.figure(figsize=(14, 6))
    scatter = plt.scatter(df['timestamp'], df['btc_price'], c=df['score'], cmap='coolwarm', s=25)
    plt.colorbar(scatter, label='Signal Score')
    plt.title("BTC Price with Signal Scores")
    plt.xlabel("Time")
    plt.ylabel("BTC Price (USD)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{save_dir}/btc_price_with_signals.png")
    plt.show()


def plot_cumulative_return(threshold=0.5):
    df = load_merged_signals_returns()
    df = df.dropna(subset=["fwd_return_1h"])
    df['position'] = (df['score'] > threshold).astype(int)
    df['strategy_return'] = df['position'] * df['fwd_return_1h']
    df['cumulative_return'] = df['strategy_return'].cumsum()
    plt.figure(figsize=(12, 6))
    plt.plot(df['timestamp'], df['cumulative_return'], label=f"Score > {threshold}")
    plt.axhline(0, color='gray', linestyle='--')
    plt.title(f"Cumulative Return (Score > {threshold})")
    plt.xlabel("Time")
    plt.ylabel("Cumulative Return (%)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{save_dir}/cumulative_return_thresh_{threshold}.png")
    plt.show()


if __name__ == "__main__":
    plot_score_histogram()
    plot_score_vs_median_fee()
    plot_score_vs_spread()
    plot_score_vs_return_scatter()
    plot_score_vs_forward_return("fwd_return_1h")
    plot_score_vs_forward_return("fwd_return_2h")
    plot_score_vs_forward_return("fwd_return_4h")
    plot_btc_price_with_signals()
    plot_cumulative_return(threshold=0.5)
