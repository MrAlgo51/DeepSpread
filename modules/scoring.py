def compute_score(median_fee, unconfirmed_tx, spread_pct, usdt_premium_z=None):
    if None in (median_fee, unconfirmed_tx, spread_pct):
        return None

    score = 0.0
    score += min(spread_pct / 1.0, 1.0) * 0.3
    score += min(median_fee / 50.0, 1.0) * 0.4
    score += min(unconfirmed_tx / 300_000, 1.0) * 0.2

    if usdt_premium_z is not None:
        score += min(max(usdt_premium_z, 0) / 3.0, 1.0) * 0.1

    return round(score, 4)
