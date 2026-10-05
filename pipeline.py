"""Repeatable data-cleaning pipeline with explicit validation rules.

Every rejected row is written to a reject file with the reason, so data
issues are visible instead of silently disappearing.
"""
from pathlib import Path

import pandas as pd

VALID_CHANNELS = {"email", "social", "search", "display"}


def clean(raw: pd.DataFrame):
    """Return (clean_df, rejects_df). Pure function so it is easy to test."""
    df = raw.copy()
    rejects = []

    def reject(mask, reason):
        nonlocal df
        if mask.any():
            bad = df[mask].copy()
            bad["reject_reason"] = reason
            rejects.append(bad)
            df = df[~mask]

    # Standardise text before validating it
    df["channel"] = df["channel"].astype("string").str.strip().str.lower()
    df["event_time"] = pd.to_datetime(df["event_time"], errors="coerce")

    reject(df.duplicated(subset="event_id", keep="first"), "duplicate event_id")
    reject(df["campaign"].isna(), "missing campaign")
    reject(df["event_time"].isna(), "invalid event_time")
    reject(~df["channel"].isin(VALID_CHANNELS), "unknown channel")
    reject(df["spend"] < 0, "negative spend")
    df["clicks"] = df["clicks"].fillna(0)  # missing clicks treated as zero, documented in README
    rejects_df = pd.concat(rejects) if rejects else pd.DataFrame()
    return df.reset_index(drop=True), rejects_df


def main():
    out = Path("output")
    out.mkdir(exist_ok=True)
    raw = pd.read_csv("data/raw_events.csv")
    clean_df, rejects = clean(raw)
    clean_df.to_csv(out / "clean_events.csv", index=False)
    rejects.to_csv(out / "rejected_rows.csv", index=False)
    print(f"Input rows : {len(raw):,}")
    print(f"Clean rows : {len(clean_df):,}")
    print(f"Rejected   : {len(rejects):,}")
    print(rejects["reject_reason"].value_counts().to_string())


if __name__ == "__main__":
    main()
