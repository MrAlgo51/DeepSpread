from datetime import datetime, timezone

def get_current_utc_timestamp():
    """
    Return current UTC timestamp in ISO 8601 format.
    Example: 2025-06-14T15:13:32+00:00
    """
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

