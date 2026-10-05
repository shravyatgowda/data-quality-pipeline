"""Generate a messy synthetic marketing/system log file (SYNTHETIC data)."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(5)
N = 20_000
df = pd.DataFrame({
    "event_id": np.arange(1, N + 1),
    "event_time": pd.to_datetime("2025-06-01") + pd.to_timedelta(rng.integers(0, 60 * 24 * 60, N), unit="m"),
    "campaign": rng.choice(["Summer Sale", "Brand", "Retargeting", "Newsletter"], N),
    "channel": rng.choice(["email", "social", "search", "display"], N),
    "spend": np.round(rng.gamma(2, 40, N), 2),
    "clicks": rng.integers(0, 500, N).astype(float),
})
df.loc[rng.choice(N, 700, replace=False), "campaign"] = None       # null attributes
df.loc[rng.choice(N, 500, replace=False), "clicks"] = np.nan
neg = rng.choice(N, 200, replace=False)
df.loc[neg, "spend"] = -df.loc[neg, "spend"]  # invalid negatives
df.loc[rng.choice(N, 300, replace=False), "channel"] = "  Email "   # inconsistent text
df["event_time"] = df["event_time"].dt.strftime("%Y-%m-%d %H:%M")
df.loc[rng.choice(N, 150, replace=False), "event_time"] = "not a date"
df = pd.concat([df, df.sample(800, random_state=2)], ignore_index=True)  # duplicates
df.to_csv("data/raw_events.csv", index=False)
print(f"Wrote data/raw_events.csv with {len(df):,} rows")
