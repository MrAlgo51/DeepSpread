import sys, os

import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'deepspread.db'))


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

SNAPSHOT_INTERVAL = 60  # seconds
SPOT_REST_URL = "https://api-pub.bitfinex.com/v2/ticker/tBTCUSD"
MARK_PRICE_WS_URL = "wss://fstream.binance.com/ws/!markPrice@arr"
