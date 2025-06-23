import pandas as pd
import matplotlib.pyplot as plt
import pytz

# Load the VWAP output CSV
file_path = "vwap_output.csv"
df = pd.read_csv(file_path, parse_dates=["timestamp"])

# Ensure required columns exist
required_cols = ["timestamp", "close", "vwap_calc"]
if not all(col in df.columns for col in required_cols):
    raise ValueError("Missing one or more required columns in vwap_output.csv")

# Convert close and vwap to float
df["close"] = df["close"].astype(float)
df["vwap_calc"] = df["vwap_calc"].astype(float)

# Convert timestamps to EST for readability
df["timestamp"] = df["timestamp"].dt.tz_localize("UTC").dt.tz_convert("US/Eastern")

# Plot close price and VWAP
plt.figure(figsize=(12, 6))
plt.plot(df["timestamp"], df["close"], label="Close Price", color="black")
plt.plot(df["timestamp"], df["vwap_calc"], label="VWAP", color="blue", linestyle="--")

# Add vertical line for DeepSpread signal (converted to EST)
signal_time_utc = pd.to_datetime("2025-06-20 06:04:00").tz_localize("UTC")
signal_time_est = signal_time_utc.astimezone(pytz.timezone("US/Eastern"))
plt.axvline(signal_time_est, color="red", linestyle=":", linewidth=2, label="DeepSpread Signal")

plt.title("BTC Price vs VWAP (Timestamps in EST)")
plt.xlabel("Timestamp (EST)")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
