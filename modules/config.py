import os

# Dynamically calculate the root project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# File save paths (absolute)
MEMPOOL_LOG_PATH = os.path.join(BASE_DIR, "data", "mempool_log.csv")
SPREAD_LOG_PATH = os.path.join(BASE_DIR, "data", "spread_log.csv")
SCORE_LOG_PATH = os.path.join(BASE_DIR, "data", "score_log.csv")

# API endpoints
KRAKEN_API = "https://api.kraken.com/0/public/Ticker?pair=XMRXBT"
TRADEOGRE_API = "https://tradeogre.com/api/v1/ticker/BTC-XMR"
MEMPOOL_API = "https://mempool.space/api/mempool"
KRAKEN_XMRUSD_URL = "https://api.kraken.com/0/public/Ticker?pair=XXMRZUSD"

# Logger settings
LOG_INTERVAL_MINUTES = 60  # for hourly cron

# Scoring thresholds
FEE_SPIKE_THRESHOLD = 1.25
SPREAD_DELTA_THRESHOLD = 1.15

# Database path
# Database path (relative to project root)
DB_PATH = os.path.join(BASE_DIR, "data", "deepspread.db")


# Database table names
USDT_PREMIUM_TABLE = "usdt_premium"
