import pandas as pd

def compute_z_score_from_series(series: pd.Series, current_value: float, window: int = 20) -> float:
    """
    Compute the z-score of `current_value` against the trailing `window` values in `series`.
    """
    series = series.dropna()
    if len(series) < window:
        return 0.0

    windowed = series[-window:]
    mean = windowed.mean()
    std = windowed.std()

    if std == 0 or pd.isna(std):
        return 0.0

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
