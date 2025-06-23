import os

# --- Project Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# File save paths (for optional CSV logging, if used)
MEMPOOL_LOG_PATH = os.path.join(BASE_DIR, "data", "mempool_log.csv")
SPREAD_LOG_PATH = os.path.join(BASE_DIR, "data", "spread_log.csv")
SCORE_LOG_PATH = os.path.join(BASE_DIR, "data", "score_log.csv")

# --- API Endpoints ---
KRAKEN_API = "https://api.kraken.com/0/public/Ticker?pair=XMRXBT"
TRADEOGRE_API = "https://tradeogre.com/api/v1/ticker/BTC-XMR"
MEMPOOL_API = "https://mempool.space/api/mempool"
KRAKEN_XMRUSD_URL = "https://api.kraken.com/0/public/Ticker?pair=XXMRZUSD"

# Bitfinex (no auth required)
BITFINEX_BTC_USD = "https://api-pub.bitfinex.com/v2/ticker/tBTCUSD"
BITFINEX_BTC_USDT = "https://api-pub.bitfinex.com/v2/ticker/tBTCUST"

# --- Scoring & Logging ---
LOG_INTERVAL_MINUTES = 60
FEE_SPIKE_THRESHOLD = 1.25
SPREAD_DELTA_THRESHOLD = 1.15

# --- Database ---
DB_PATH = os.path.join(BASE_DIR, "data", "deepspread.db")

# --- Table names (for clarity and reuse if needed) ---
USDT_PREMIUM_TABLE = "usdt_premium"
