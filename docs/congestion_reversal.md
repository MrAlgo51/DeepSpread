**DeepSpread Case Study: Congestion Reversal Pattern – June 16, 2025**

---

### Summary

This case captures a full congestion-driven breakout and subsequent reversal, logged from 18:00 UTC to 01:00 UTC on June 16–17. It represents a near textbook example of how elevated mempool pressure can fuel upside in BTC, and how the removal of that pressure can lead to exhaustion and mean reversion.

---

### Timeline Overview

| Time (UTC) | Median Fee (sats/vB) | Spread % | Spread Z | BTC Price | Notes                           |
| ---------- | -------------------- | -------- | -------- | --------- | ------------------------------- |
| 18:04      | 14,928               | +0.27%   | +1.98    | \$107,800 | Strong score, breakout move     |
| 19:04      | 14,540               | -0.44%   | +0.31    | \$108,333 | Still strong, spread tightening |
| 20:04      | 12,728               | -0.33%   | +0.50    | \$108,583 | Price stalls, congestion falls  |
| 21:04      | 6,673                | -0.86%   | -0.70    | \$108,813 | Top tick; fee collapse begins   |
| 22:04      | 8,146                | +0.13%   | +1.65    | \$108,709 | Spread spikes positive again    |
| 23:04      | 9,134                | -0.89%   | -0.73    | \$107,640 | Price fades, trend breaks       |
| 01:04      | 6,981                | -1.02%   | -0.94    | \$107,215 | Full reversal confirmed         |

---

### Key Insights

**1. Mempool Exhaustion as a Top Signal**
The rise from \$107.8K to \$108.8K was accompanied by elevated median fees (\~15K sats/vB). Once those fees dropped below \~7K, the move lost momentum, suggesting that **fee compression is a key reversal indicator**.

**2. Spread Behavior Reinforced the Move**
Spread % went from +0.27% → -0.89% in under 5 hours. A positive spike at 22:00 coincided with distribution, not trend strength.

This suggests **spread re-expansion after congestion may signal instability or exit.**

**3. Score Worked (Directional Validity)**
DeepSpread score peaked at 0.0277 at 18:04. As congestion fell, so did the score. It declined to \~0.0044 near the top, then stabilized.

While not predictive on its own, the score correctly flagged **high-pressure zones** — its decline mirrored **liquidity draining** from the move.

---

### Tentative Trade Logic

If this pattern repeats, potential short-side logic may look like:

* **Entry Trigger**: Score > 0.02, median fee > 10K, price trending up
* **Reversal Trigger**: Median fee drops > 40% from peak within 2–3 hours
* **Confirmation**: Spread % tightens or flips negative
* **Action**: Exit long / consider short when reversal confirmed

---

### Status

**Not yet confirmed as reliable.** This case should be logged as the first clean congestion reversal pattern. More data required to test robustness.

---

### Tag

`#case_study #reversal #congestion #spread #score #June16`
