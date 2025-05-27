import csv
import datetime
import os

def read_last_row(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if len(lines) < 2:
            return None
        return lines[-1].strip().split(',')

mempool_row = read_last_row('mempool_log.csv')
spread_row = read_last_row('spread_log.csv')

if not mempool_row or not spread_row:
    print("[SKIP] Missing data, cannot score.")
else:
    mem_ts = datetime.datetime.strptime(mempool_row[0], '%Y-%m-%d %H:%M:%S UTC')
    spd_ts = datetime.datetime.strptime(spread_row[0], '%Y-%m-%d %H:%M:%S UTC')

    # Allow up to 60 seconds difference
    time_diff = abs((mem_ts - spd_ts).total_seconds())

    if time_diff <= 60:
        mem_tx_count = int(mempool_row[1])
        mem_size = int(mempool_row[2])
        spread_val = float(spread_row[3])

        # Example scoring function
        score = (mem_tx_count / 20000) + (mem_size / 1e7) + (spread_val / 100)

        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        with open('score_log.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if os.stat('score_log.csv').st_size == 0:
                writer.writerow(['Timestamp', 'TX Count', 'Mempool Size', 'Spread', 'Score'])
            writer.writerow([timestamp, mem_tx_count, mem_size, spread_val, round(score, 4)])

        print(f"[{timestamp}] Score: {round(score, 4)}")
    else:
        print(f"[SKIP] Timestamps too far apart ({time_diff:.1f} sec)")
