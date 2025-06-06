import sqlite3

DB_PATH = "data/deepspread.db"

def cleanup_signals():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # DELETE rows where any of these key values are zero
    cursor.execute("""
        DELETE FROM signals
        WHERE btc_price = 0
           OR spread_pct = 0
           OR median_fee = 0
    """)
    
    deleted = conn.total_changes
    conn.commit()
    conn.close()

    print(f"[CLEANUP] Deleted {deleted} low-quality rows from 'signals' table.")

if __name__ == "__main__":
    cleanup_signals()
