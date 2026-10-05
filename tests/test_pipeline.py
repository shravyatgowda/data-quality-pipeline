import pandas as pd
from pipeline import clean


def make(**kw):
    base = dict(event_id=1, event_time="2025-06-01 10:00", campaign="Brand",
                channel="email", spend=10.0, clicks=5.0)
    base.update(kw)
    return pd.DataFrame([base])


def test_valid_row_passes():
    df, rej = clean(make())
    assert len(df) == 1 and rej.empty


def test_duplicate_removed():
    raw = pd.concat([make(), make()], ignore_index=True)
    df, rej = clean(raw)
    assert len(df) == 1 and (rej.reject_reason == "duplicate event_id").all()


def test_null_campaign_rejected():
    df, rej = clean(make(campaign=None))
    assert df.empty and rej.reject_reason.iloc[0] == "missing campaign"


def test_channel_is_standardised():
    df, _ = clean(make(channel="  Email "))
    assert df.channel.iloc[0] == "email"


def test_negative_spend_rejected():
    df, rej = clean(make(spend=-5.0))
    assert df.empty and rej.reject_reason.iloc[0] == "negative spend"
