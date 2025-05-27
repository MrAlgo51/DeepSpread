import requests
import csv
from datetime import datetime

# === Get mempool data from mempool.space ===
try:
    response = requests.get("https://mempool.space/api/mempool")
    response.raise_for_status()
    data = response.json()
except Exception as e:
    print(f"[ERROR] Failed to fetch mempool data: {e}")
    exit()

# === Extract key metrics ===
timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
tx_count = data.get("count", 0)
total_vbytes = data.get("vsize", 0)

# === Save to CSV ===
csv_file = "logs/mempool_log.csv"

try:
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write header if file is empty
        if file.tell() == 0:
            writer.writerow(["timestamp", "tx_count", "total_vbytes"])
        writer.writerow([timestamp, tx_count, total_vbytes])
    print(f"[{timestamp}] TXs: {tx_count} | Size: {total_vbytes} vBytes")
except Exception as e:
    print(f"[ERROR] Failed to write to CSV: {e}")
