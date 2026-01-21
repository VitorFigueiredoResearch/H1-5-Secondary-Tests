"""
H1.5 — RAR Diagnostic Plot
Compare H1-predicted RAR to Newtonian and standard empirical RAR.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --- PATHS ---
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR   = SCRIPT_DIR.parent / "data" / "h1_frozen_results"
FILE_IN    = DATA_DIR / "rar_points.csv"
PLOT_OUT   = DATA_DIR / "rar_diagnostic.png"

# --- LOAD DATA ---
df = pd.read_csv(FILE_IN)

# --- UNIT CONVERSION ---
# 1 (km/s)^2 / kpc = 3.24078e-14 m/s^2
CONVERSION = 3.24078e-14

df["g_bar_SI"] = df["g_bar"] * CONVERSION
df["g_obs_SI"] = df["g_obs"] * CONVERSION

# Log-safe filter
df = df[(df["g_bar_SI"] > 0) & (df["g_obs_SI"] > 0)]

x = np.log10(df["g_bar_SI"].values)
y = np.log10(df["g_obs_SI"].values)

# --- PLOT ---
plt.style.use("dark_background")
fig, ax = plt.subplots(figsize=(10, 8), dpi=200)

hb = ax.hexbin(
    x, y,
    gridsize=60,
    bins="log",
    cmap="magma",
    mincnt=1
)

cb = fig.colorbar(hb, ax=ax)
cb.set_label("log10(point density)")

# Newtonian 1:1 line
lims = [x.min(), x.max()]
ax.plot(lims, lims, "--", color="white", alpha=0.4, label="Newtonian (no DM)")

# Standard empirical RAR (MOND-like)
a0 = 1.2e-10  # m/s^2
gb = np.logspace(x.min(), x.max(), 300)
go = gb / (1 - np.exp(-np.sqrt(gb / a0)))

ax.plot(
    np.log10(gb),
    np.log10(go),
    color="lime",
    lw=2.5,
    label="Empirical RAR (SPARC/MOND)"
)

ax.set_xlabel(r"$\log_{10}(g_{\mathrm{bar}})\;[m/s^2]$")
ax.set_ylabel(r"$\log_{10}(g_{\mathrm{obs}})\;[m/s^2]$")
ax.set_title("H1.5 — Radial Acceleration Relation (Diagnostic)")

ax.legend()
ax.grid(alpha=0.15, linestyle=":")

plt.tight_layout()
plt.savefig(PLOT_OUT)
plt.close()

print("-" * 60)
print(f"RAR plot saved to: {PLOT_OUT}")
print(f"Points plotted: {len(df)}")
print("-" * 60)
