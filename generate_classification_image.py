"""
Generate a classification comparison image for the JMU location_count data.
Mirrors the style of the reference Quantile / Equal / Jenks histogram panels.
Run from the workspace root:
    python generate_classification_image.py
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import mapclassify

# Load data and apply the same correction pipeline used in the notebook
df = pd.read_csv("data/JMU/JMU_geoparsed_long.csv")
_df = df[df["action"] != "REMOVE"].copy()
_mask = _df["action"] == "CORRECT"
_has_name = _mask & _df["corrected_name"].fillna("").str.strip().ne("")
_df.loc[_has_name, "place"] = _df.loc[_has_name, "corrected_name"]

counts = (
    _df.dropna(subset=["place", "latitude", "longitude"])
    .groupby("place")
    .size()
    .astype(int)
)
data_min = int(counts.min())
data_max = int(counts.max())

K = 4  # number of classes

# Compute breaks
_, q_edges = pd.qcut(counts, q=K, duplicates="drop", retbins=True)
q_breaks = q_edges.copy(); q_breaks[0] = data_min; q_breaks[-1] = data_max
ei_breaks = np.linspace(data_min, data_max, K + 1)
jnb = mapclassify.NaturalBreaks(counts.values, k=K)
j_breaks = np.concatenate([[data_min], jnb.bins]); j_breaks[-1] = data_max

ALL_COLORS = ["#c7e9b4", "#74c476", "#238b45", "#00441b"]
def pick_colors(n):
    idx = np.round(np.linspace(0, len(ALL_COLORS) - 1, n)).astype(int)
    return [ALL_COLORS[i] for i in idx]

fig, axes = plt.subplots(3, 1, figsize=(7, 10))
fig.patch.set_facecolor("white")

HIST_BINS  = 25
BAND_FRAC  = 0.10
LABEL_FRAC = 0.28
methods = [("Quantile", q_breaks), ("Equal", ei_breaks), ("Jenks", j_breaks)]

for ax, (name, breaks) in zip(axes, methods):
    n, _, _ = ax.hist(counts, bins=HIST_BINS, color="#F4C78A",
                      edgecolor="white", linewidth=0.4)
    y_top   = max(n) * 1.12
    band_h  = y_top * BAND_FRAC
    label_h = y_top * LABEL_FRAC

    ax.set_ylim(-(band_h + label_h), y_top)
    ax.set_xlim(data_min - 1, data_max * 1.015)

    ax.vlines(counts, 0, y_top * 0.025, color="#8B4513",
              alpha=0.55, linewidth=0.9, zorder=4)

    n_cls  = len(breaks) - 1
    colors = pick_colors(n_cls)
    for i in range(n_cls):
        ax.add_patch(mpatches.Rectangle(
            (breaks[i], -band_h), breaks[i + 1] - breaks[i], band_h,
            linewidth=0, facecolor=colors[i]))

    # Draw lines from bottom of band to top of histogram — stop before tick labels
    ax.vlines(breaks, -band_h, y_top, color="black", linewidth=1.1, zorder=5)

    ax.axhline(0, color="#cccccc", linewidth=0.6, zorder=3)
    ax.spines["bottom"].set_position(("data", -band_h))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_bounds(0, y_top)

    step = 50 if y_top > 100 else 25
    ax.set_yticks(np.arange(0, y_top + 1, step))
    ax.tick_params(axis="y", labelsize=8)
    ax.set_xticks(breaks)
    ax.set_xticklabels([str(int(b)) for b in breaks], rotation=90, fontsize=8)
    ax.tick_params(axis="x", pad=3)
    ax.set_title(name, fontweight="bold", fontsize=11, pad=5)
    ax.set_ylabel("# of places", fontsize=9)

plt.tight_layout(h_pad=2.0)
out_path = "lesson_assets/images/classification_methods.png"
plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print(f"Saved -> {out_path}")
