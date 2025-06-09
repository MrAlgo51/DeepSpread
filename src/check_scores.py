import sqlite3

# Manually set the absolute path to your database
DB_PATH = r"C:\Users\cweat\OneDrive\Desktop\DeepSpread_CLEANED\DeepSpread\data\deepspread.db"

def show_latest_scores(n=5):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT timestamp, score, btc_price, spread_pct, median_fee, unconfirmed_tx
        FROM signals
        ORDER BY timestamp DESC
        LIMIT ?
    """, (n,))
    rows = cursor.fetchall()
    conn.close()

    print(f"\nLatest {n} entries in signals:\n")
    for row in rows:
        print(f"🕓 {row[0]} | 🧮 Score: {row[1]:.4f} | 🟠 BTC: {row[2]} | Spread: {row[3]:.2f}% | Fee: {row[4]} | TXs: {row[5]}")

if __name__ == "__main__":
    show_latest_scores()
