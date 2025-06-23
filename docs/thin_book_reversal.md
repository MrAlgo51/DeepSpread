# Thin Book Reversal – Rule Draft

## ⏱️ Observed Timestamp
**UTC:** 2025-06-16T22:04  
**Local (New York):** 6:04 PM, Sunday night

---

## 📊 Logged Metrics at Signal

| Metric              | Value            |
|---------------------|------------------|
| Median Fee          | ~12 sats/vByte   |
| Mempool Size        | ~2.2 million vBytes |
| Unconfirmed TXs     | ~5764            |
| Pressure Score      | ~0.43            |
| USDT Premium Z-Score | 0.0             |
| BTC/XMR Spread Z-Score | ~-0.8         |

---

## 📈 Price Behavior

- Price made a **local low** near the signal timestamp
- Reversed and climbed steadily for the next several hours
- Appeared to react to **congestion easing** and potential thin book dynamics

---

## 🧠 Interpretive Notes

- Sunday night: thin liquidity could amplify movements.
- Despite no "extreme" signal values, a **cluster of mild congestion** readings plus a **low USDT premium** may have coincided with a turning point.
- BTC price was sitting on multi-day support and rebounded post-event.

---

## 🧪 Draft Rule (V1)

```python
IF (median_fee > 10)
AND (unconfirmed_tx > 5000)
AND (pressure_score > 0.4)
AND (spread_z < 0)
AND (usdt_premium_z < 0.1)
THEN
    Tag: "Thin Book Congestion Reversal"
    Action: Watch for reversal within 1–3 candles
