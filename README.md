# DeepSpread

**DeepSpread** is a Bitcoin signal research engine. It monitors the mempool, perpetual funding rates, underground market spreads, and stablecoin premiums to detect moments of rare market stress or crowding. It logs all metrics to SQLite and assigns a composite score (0–1) for each timestamp.

This is not a trading bot — it’s a modular signal framework for quant research and edge development.

---

## 🔧 Project Structure

<pre>DeepSpread/
├── data/
│   └── deepspread.db               # SQLite database storing all logged data
│
├── modules/
│   ├── config.py                   # Central config (DB path, thresholds, etc.)
│   ├── scoring.py                 # Combines signals into a composite score
│   ├── error_logger.py            # Logs errors to file for debugging
│   ├── fetchers.py                # Kraken BTC/USD + other API fetchers
│   ├── binance_ws.py              # Live Binance mark price + funding WebSocket
│   ├── data_utils.py              # Timestamp alignment, forward returns, etc.
│
├── src/
│   ├── merged_logger.py           # Main signal logger combining all inputs
│   ├── binance_premium_ws_logger.py # Logs funding/mark data from Binance
│   ├── mempool_logger.py          # Logs mempool stats (median fee, tx count, etc.)
│   ├── analyzer.py                # Score performance analysis, return buckets
│   ├── visualizer.py              # Charts for score-return relationships
│   ├── usdt_premium_logger.py     # Logs USDT premium and z-score
│
├── logs/
│   └── *.log                      # Optional log files per module
│
├── README.md                      # This file
├── requirements.txt               # Python dependencies
└── .gitignore                     # Ignores `__pycache__`, `.db`, `.log`, etc.
</pre>

---

## ⚙️ How It Works

1. **Live Logging**
   - `binance_premium_ws_logger.py` connects to Binance and logs:
     - BTCUSDT mark price
     - BTC spot price from Bitfinex
     - Funding rate
     - Premium %
   - `mempool_logger.py` logs:
     - Median mempool fee
     - Unconfirmed transaction count
     - Mempool vSize
     - Low-fee block estimate
   - `usdt_premium_logger.py` logs:
     - BTC/USDT - BTC/USD premium %
     - Z-score of premium

2. **Signal Scoring**
   - `merged_logger.py` pulls the latest values from all tables
   - Computes a `score` using congestion, spread, and premium metrics
   - Logs to the `signals` table

3. **Forward Return Analysis**
   - `analyzer.py` computes forward returns at 1h, 2h, 4h for each signal timestamp
   - Evaluates return by score bucket, congestion regime, etc.

4. **Visualization**
   - `visualizer.py` graphs:
     - Score vs return scatterplots
     - Equity curves by threshold
     - Congestion overlays and more

---

## 🧠 Unified Signal Decoder

| Column / Term      | Description                                                      |
|--------------------|------------------------------------------------------------------|
| `btc_price`        | BTC/USD spot from Kraken                                         |
| `funding_rate`     | Binance BTCUSDT predicted funding rate (8h %)                    |
| `median_fee`       | Median transaction fee (sats/vByte) from mempool.space           |
| `unconfirmed_tx`   | Total pending TXs in the mempool                                 |
| `spread_pct`       | BTC/XMR price spread — Kraken BTCUSD vs XMRUSD                   |
| `spread_delta`     | 1-period % change in BTC/XMR spread                              |
| `usdt_premium_pct` | Raw premium (Binance BTC/USDT - Kraken BTC/USD) / Kraken BTC/USD |
| `usdt_premium_z`   | Z-score of USDT premium vs recent average                        |
| `score`            | Weighted stress score (0–1) combining all of the above           |
| `signals` table    | Unified record of all logged metrics per timestamp               |

---

## 🗃️ Database Schema (SQLite)

All logs are written to `data/deepspread.db`.

### Table: `signals`
| Column             | Type    | Description                                          |
|--------------------|---------|------------------------------------------------------|
| timestamp          | TEXT    | UTC timestamp                                        |
| btc_price          | REAL    | Kraken BTC/USD spot price                            |
| funding_rate       | REAL    | Binance BTCUSDT funding rate                         |
| median_fee         | REAL    | Mempool median fee (sats/vByte)                      |
| unconfirmed_tx     | INTEGER | Count of unconfirmed transactions                    |
| spread_pct         | REAL    | BTC/XMR spread (Kraken)                              |
| spread_delta       | REAL    | Change in BTC/XMR spread                             |
| usdt_premium_pct   | REAL    | BTC/USDT vs BTC/USD premium %                        |
| usdt_premium_z     | REAL    | Z-score of premium                                   |
| score              | REAL    | Final computed signal score (0–1)                    |

### Table: `binance_premium`
| timestamp     | mark_price | spot_price | funding_rate | premium_pct |
|---------------|------------|------------|---------------|-------------|

### Table: `mempool_logs`
| timestamp     | median_fee | mempool_size | low_fee_blocks | unconfirmed_tx |

### Table: `usdt_premium`
| timestamp     | premium_pct | premium_z |

### Table: `returns`
| timestamp     | return_1h | return_2h | return_4h | price_now |

---

## ✅ Status

- ✅ Real-time logging
- ✅ SQLite integration
- ✅ Composite signal scoring
- ✅ Forward return tracking
- ✅ Basic visualizations and scatterplots
- 🔜 Threshold optimization and alerts

---

## 👤 Author

**DeepSpread** is a solo-built market research system for stress signal discovery in crypto markets.  
Designed for self-hosted quant trading, non-KYC environments, and long-term edge development.

Star it. Fork it. Or ignore it. But don’t say you weren’t warned.
