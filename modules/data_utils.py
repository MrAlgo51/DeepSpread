# modules/data_utils.py

import sqlite3
from datetime import datetime, timedelta
from modules import config

def get_closest_mempool_row(target_ts_str, window_seconds=60):
    """
    Find the closest mempool row to the given timestamp (±window_seconds).
    """
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()

    # Convert string timestamp to datetime object
    target_ts = datetime.strptime(target_ts_str, "%Y-%m-%d %H:%M:%S UTC")
    lower_bound = (target_ts - timedelta(seconds=window_seconds)).strftime("%Y-%m-%d %H:%M:%S UTC")
    upper_bound = (target_ts + timedelta(seconds=window_seconds)).strftime("%Y-%m-%d %H:%M:%S UTC")

    query = """
        SELECT *, ABS(strftime('%s', timestamp) - strftime('%s', ?)) AS time_diff
        FROM mempool
        WHERE timestamp BETWEEN ? AND ?
        ORDER BY time_diff ASC
        LIMIT 1
    """
    cursor.execute(query, (target_ts_str, lower_bound, upper_bound))
    row = cursor.fetchone()
    conn.close()

    return row  # None if no match
