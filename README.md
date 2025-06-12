# DeepSpread

DeepSpread is an exploratory Bitcoin swing trading research tool. It analyzes network congestion and underground market spreads to identify rare stress signals in the Bitcoin ecosystem.

This project is not a bot. It does not auto-trade. It’s a research and signal generation system built in Python using SQLite for storage and matplotlib/pandas for analysis.

---
'''
DeepSpread/
├── data/
│   └── deepspread.db               # SQLite database storing all logged data
│
├── modules/
│   ├── config.py                   # Central config (DB path, thresholds, etc.)
│   ├── data_utils.py              # Utility functions (e.g., timestamp alignment)
│   ├── error_logger.py            # Logs errors to file for debugging
│   ├── fetch_kraken_spread.py     # Fetch BTC/XMR spread (Kraken)
│   ├── fetch_tradeogre_xmrbtc.py  # Fetch XMR/BTC price from TradeOgre (optional)
│   ├── fetch_kraken_btcusd.py     # Kraken BTC/USD price
│   ├── fetch_coingecko_btcusd.py  # Coingecko USDT price (Binance proxy)
│   ├── scoring.py                 # Combines signals into a composite score
│   ├── path_setup.py              # Ensures Python paths are correctly set
│
├── src/
│   ├── analyzer.py                # Generates forward returns + performance analysis
│   ├── visualizer.py              # Score-return charts, histograms, signal overlays
│   ├── score_logger.py            # Logs the final DeepSpread score
│   ├── mempool_logger.py          # Logs mempool stats (median fee, size, etc.)
│   ├── spread_logger.py           # Logs BTC/XMR spread and z-score
│   ├── usdt_premium_logger.py     # Logs BTC/USD vs USDT price premium and z-score
│   ├── run_all.py (optional)      # Executes all loggers sequentially
│
├── logs/
│   └── *.log                      # Error logs from each module (optional)
│
├── README.md                      # Project overview, install, and workflow
├── requirements.txt               # Python dependencies (optional)
└── .gitignore                     # Ignores `__pycache__`, `.db`, `.log`, etc.'''



## How It Works

1. **Signal Logging**  
   Every hour, DeepSpread fetches and logs the following metrics:
   - BTC/XMR spread across Kraken and TradeOgre
   - Median mempool fee (sats/vByte)
   - Unconfirmed transaction count
   - BTC/USDT premium (% difference vs BTC/USD)
   - BTC price

2. **Scoring System**  
   These metrics are scored using custom thresholds and combined into a single score (0 to 1) that represents market “stress.” The higher the score, the more unusual or congested the market state.

3. **Forward Returns**  
   For each score event, DeepSpread logs forward BTC price returns at 1h, 2h, and 4h horizons. This enables data-driven analysis of signal quality.

4. **Analysis Module**  
   Run `analyzer.py` to:
   - View performance by score bucket
   - Find optimal thresholds
   - Export CSV summaries

---

## Database Schema (SQLite)

All data is stored in `data/deepspread.db`.

### Table: `signals`

| Column         | Type    | Description                                 |
|----------------|---------|---------------------------------------------|
| timestamp      | TEXT    | UTC timestamp (primary key)                 |
| score          | REAL    | Final DeepSpread score                      |
| btc_price      | REAL    | BTC/USD price at time of signal             |
| spread_pct     | REAL    | Kraken vs TradeOgre BTC/XMR spread %        |
| median_fee     | REAL    | Mempool median fee in sats/vByte            |
| unconfirmed_tx | INTEGER | Count of unconfirmed transactions           |
| usdt_premium   | REAL    | % premium of BTC/USDT over BTC/USD          |
| premium_zscore | REAL    | Z-score of BTC/USDT premium                 |

### Table: `returns`

| Column       | Type  | Description                      |
|--------------|-------|----------------------------------|
| timestamp    | TEXT  | Matches `signals.timestamp`      |
| return_1h    | REAL  | Forward return in 1 hour         |
| return_2h    | REAL  | Forward return in 2 hours        |
| return_4h    | REAL  | Forward return in 4 hours        |
| price_now    | REAL  | BTC price at time of signal      |

---

## Status

✅ Logging works  
✅ SQLite integration complete  
✅ Analyzer produces valid score buckets  
⏳ Visualizer under development  
⏳ Rule testing (v1.5) in progress

---

## Author

This is a solo project, designed for high-signal, censorship-resistant market research. If you use this repo, fork it, or build on it, drop a star.
