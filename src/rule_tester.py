import sqlite3
import pandas as pd
import json
import itertools

DB_PATH = "data/deepspread.db"
CONFIG_PATH = "config/rule_config.json"

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def tag_congestion(fee):
    if fee < 2:
        return "quiet"
    elif fee < 5:
        return "normal"
    else:
        return "congested"

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df_signals = pd.read_sql_query("SELECT * FROM signals", conn)
    df_returns = pd.read_sql_query("SELECT * FROM returns", conn)
    conn.close()

    # Drop duplicate score column if it exists in both
    if 'score' in df_returns.columns:
        df_returns = df_returns.drop(columns=['score'])

    # Merge and clean
    df = pd.merge(df_signals, df_returns, on="timestamp")
    df = df.replace([float("inf"), float("-inf")], pd.NA)
    df = df.dropna(subset=["return_1h", "return_2h", "return_4h"])

    # Optional: tag congestion
    df["congestion"] = df["median_fee"].apply(tag_congestion)

    return df



def evaluate_rule(df, rule_name, logic, sweep_values):
    keys = sweep_values.keys()
    all_combos = list(itertools.product(*sweep_values.values()))

    results = []
    for combo in all_combos:
        rule_expr = logic
        params = {}
        for k, v in zip(keys, combo):
            rule_expr = rule_expr.replace(f"{{{k}}}", str(v))
            params[k] = v

        try:
            df_filtered = df.query(rule_expr)
        except Exception as e:
            print(f"[ERROR] Bad expression: {rule_expr} | {e}")
            continue

        n = len(df_filtered)
        print(f"[DEBUG] Rule: {rule_expr} | Matches: {n}")
        if n == 0:
            continue

        avg_return = df_filtered["return_1h"].mean()
        win_rate = (df_filtered["return_1h"] > 0).mean()

        results.append({
            "rule": rule_name,
            "logic": rule_expr,
            "n": n,
            "avg_return_1h": avg_return,
            "win_rate": win_rate,
            **params
        })

    return results

def run_rule_tests():
    config = load_config()
    df = load_data()
    all_results = []

    for rule in config["rules"]:
        name = rule["name"]
        logic = rule["logic"]
        sweep = rule["sweep"]
        results = evaluate_rule(df, name, logic, sweep)
        all_results.extend(results)

    df_results = pd.DataFrame(all_results)
    sort_field = config.get("sort_by", "avg_return_1h")
    df_results = df_results.sort_values(by=sort_field, ascending=False)

    print(df_results.head(15))
    df_results.to_csv("rule_test_results.csv", index=False)
    print("Saved to rule_test_results.csv")

    # ✅ DEBUG block inside __main__ scope
    df_recent = df[["timestamp", "score", "median_fee", "return_1h"]].sort_values(by="timestamp", ascending=False)
    print("\n=== RECENT SIGNALS ===")
    print(df_recent.head(10))

if __name__ == "__main__":
    run_rule_tests()
