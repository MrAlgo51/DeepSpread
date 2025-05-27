import requests
import csv
import datetime

def log_mempool_stats():
    try:
        response = requests.get("https://mempool.space/api/mempool", timeout=10)
        data = response.json()

        tx_count = data.get("count")
        mempool_size = data.get("vsize")

        if tx_count is None or mempool_size is None:
            print("[SKIPPED] Incomplete data, not logging.")
            return

        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

        with open("mempool_log.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, tx_count, mempool_size])

        print(f"[{timestamp}] TXs: {tx_count} | Size: {mempool_size} vBytes")

    except Exception as e:
        print(f"[ERROR] mempool fetch failed: {e}")

if __name__ == "__main__":
    log_mempool_stats()
