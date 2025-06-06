import sqlite3
import pandas as pd

conn = sqlite3.connect("data/deepspread.db")
df = pd.read_sql_query("SELECT return_1h FROM returns", conn)

print(df['return_1h'].describe())
print("\nValue counts:\n", df['return_1h'].value_counts().head(10))

