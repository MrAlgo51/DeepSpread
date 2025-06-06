import sqlite3
import pandas as pd

# Connect to DB
conn = sqlite3.connect("data/deepspread.db")

# Join signals + returns
query = """
SELECT
    r.timestamp,
    r.return_1h,
    s.score,
    s.median_fee
FROM returns r
JOIN signals s ON r.timestamp = s.timestamp
"""
df = pd.read_sql(query, conn)

# Create score buckets
df["score_bucket"] = (df["score"] // 0.1) * 0.1
df["score_bucket"] = df["score_bucket"].round(1)

# Define fee congestion label
def fee_label(fee):
    if fee >= 5:
        return "congested"
    elif fee < 2:
        return "quiet"
    else:
        return "normal"

df["fee_state"] = df["median_fee"].apply(fee_label)

# Group + summarize
grouped = df.groupby(["score_bucket", "fee_state"]).agg(
    count=("return_1h", "count"),
    avg_return_1h=("return_1h", "mean"),
    win_rate=("return_1h", lambda x: (x > 0).mean())
).reset_index()

# Print summary
print(grouped.sort_values(by=["score_bucket", "fee_state"]))
conn.close()
