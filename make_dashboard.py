"""Create a static data-quality summary image from pipeline.py outputs.

This is a Python (matplotlib) visual, NOT a Power BI report. Run pipeline.py first.
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

raw = pd.read_csv("data/raw_events.csv")
clean = pd.read_csv("output/clean_events.csv")
rej = pd.read_csv("output/rejected_rows.csv")
Path("images").mkdir(exist_ok=True)

fig = plt.figure(figsize=(13, 6.5))
fig.suptitle("Data Quality Pipeline: Summary (synthetic data, Python-generated)",
             fontsize=14, fontweight="bold")
gs = fig.add_gridspec(2, 3, height_ratios=[0.6, 2], hspace=0.5, wspace=0.4)

kpis = [("Input rows", f"{len(raw):,}"), ("Clean rows", f"{len(clean):,}"),
        ("Rejected", f"{len(rej):,} ({len(rej)/len(raw):.1%})")]
for i, (label, val) in enumerate(kpis):
    ax = fig.add_subplot(gs[0, i]); ax.axis("off")
    ax.text(.5, .62, val, ha="center", fontsize=22, fontweight="bold", color="#1f4e79")
    ax.text(.5, .12, label, ha="center", fontsize=11, color="#555")

ax = fig.add_subplot(gs[1, :2])
rej.reject_reason.value_counts().sort_values().plot(kind="barh", ax=ax, color="#c0504d")
ax.set_title("Rejected rows by reason"); ax.set_xlabel("rows")

ax = fig.add_subplot(gs[1, 2])
clean.groupby("channel").spend.sum().sort_values().plot(kind="barh", ax=ax, color="#4f81bd")
ax.set_title("Clean spend by channel")

plt.savefig("images/dashboard_summary.png", dpi=130, bbox_inches="tight")
print("Saved images/dashboard_summary.png")
