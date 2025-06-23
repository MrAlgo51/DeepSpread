import pandas as pd

def compute_z_score_from_series(series, current_value, window=20):
    if len(series) < 2:
        return None  # Not enough data to compute z-score

    if len(series) > window:
        series = series[-window:]

    mean = series.mean()
    std = series.std(ddof=0)  # Use population std

    if pd.isna(mean) or pd.isna(std):
        return None

    if std == 0:
        return 0

    return (current_value - mean) / std


def compute_score(median_fee, unconfirmed_tx, spread_z=None, usdt_premium_z=None):
    if None in (median_fee, unconfirmed_tx):
        return None

    score = 0.0
    score += min(median_fee / 50.0, 1.0) * 0.4
    score += min(unconfirmed_tx / 300_000, 1.0) * 0.2

    if spread_z is not None:
        score += min(max(spread_z, 0) / 3.0, 1.0) * 0.2

    if usdt_premium_z is not None:
        score += min(max(usdt_premium_z, 0) / 3.0, 1.0) * 0.2

    return round(score, 4)

def score_signal(funding_rate, median_fee=0, unconfirmed_tx=0, spread_pct=0, spread_delta=0):
    score = 0
    if funding_rate is None:
        return None

    if funding_rate < -0.01:
        score += 0.7
    elif funding_rate > 0.01:
        score -= 0.5

    return round(score, 3)
