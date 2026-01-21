"""
H1.5 — RAR Scatter by Radial Regime
Quantify scatter in inner / mid / outer disk regions.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# --- PATHS ---
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR   = SCRIPT_DIR.parent / "data" / "h1_frozen_results"
FILE_IN    = DATA_DIR / "rar_points.csv"

df = pd.read_csv(FILE_IN)

# Log-space residuals
log_gb = np.log10(df["g_bar"])
log_go = np.log10(df["g_obs"])
residuals = log_go - log_gb

df["residual"] = residuals

# Define regimes
regimes = {
    "Inner (r < 0.3)": df[df["r_frac"] < 0.3],
    "Mid (0.3–0.7)": df[(df["r_frac"] >= 0.3) & (df["r_frac"] < 0.7)],
    "Outer (r ≥ 0.7)": df[df["r_frac"] >= 0.7],
}

print("-" * 60)
print("RAR Scatter by Radial Regime (H1.5)")
print("-" * 60)

for name, sub in regimes.items():
    if len(sub) == 0:
        continue
    rms = np.sqrt(np.mean(sub["residual"]**2))
    med = np.median(np.abs(sub["residual"]))
    print(f"{name:18s} | N = {len(sub):4d} | RMS = {rms:.3f} dex | Median = {med:.3f} dex")

print("-" * 60)
