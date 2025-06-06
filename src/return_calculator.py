def calculate_forward_returns(df, horizons=[1, 2, 4]):
    df = df.sort_values("timestamp")
    df["price_now"] = df["btc_price"]

    # ✅ DROP rows where price_now == 0
    df = df[df["price_now"] > 0]

    for h in horizons:
        df[f"return_{h}h"] = df["price_now"].shift(-h) / df["price_now"] - 1

    # ✅ Remove inf/nan from bad divisions (shouldn’t exist anymore, but just in case)
    for h in horizons:
        col = f"return_{h}h"
        df[col].replace([np.inf, -np.inf], np.nan, inplace=True)

    return df[["timestamp"] + [f"return_{h}h" for h in horizons] + ["price_now"]]
