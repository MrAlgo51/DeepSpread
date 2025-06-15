# modules/data_utils.py

import sqlite3
from datetime import datetime, timedelta
from modules import config

def get_closest_mempool_row(target_ts_str, window_seconds=60):
    """
    Find the closest mempool row from mempool_logs to the given timestamp (±window_seconds).
    """
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM mempool_logs
        WHERE ABS(strftime('%s', timestamp) - strftime('%s', ?)) <= ?
        ORDER BY ABS(strftime('%s', timestamp) - strftime('%s', ?))
        LIMIT 1
    """, (target_ts_str, window_seconds, target_ts_str))
    row = cursor.fetchone()
    conn.close()
    return row


def get_current_utc_timestamp():
    """Returns current UTC time in standardized string format."""
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
