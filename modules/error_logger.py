from datetime import datetime
import os

ERROR_LOG_PATH = "logs/error_log.txt"

def log_error(source, message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [{source}] {message}\n"

    # Make sure the logs folder exists
    os.makedirs(os.path.dirname(ERROR_LOG_PATH), exist_ok=True)

    with open(ERROR_LOG_PATH, "a") as f:
        f.write(log_entry)
import os
from datetime import datetime, timezone

def log_to_file(source, message):
    log_dir = "logs"  # Folder where we store logs
    os.makedirs(log_dir, exist_ok=True)  # Create it if it doesn't exist
    log_path = os.path.join(log_dir, "DeepSpread.log")  # Full path to log file

    # Create a timestamp with UTC time
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    # Format the log line
    log_entry = f"[{timestamp}] [{source}] {message}\n"

    # Append the line to the log file
    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(log_entry)
