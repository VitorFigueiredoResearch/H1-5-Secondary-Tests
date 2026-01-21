import numpy as np
import pandas as pd
from pathlib import Path

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "h1_frozen_results"
RAR_FILE = DATA_DIR / "rar_points.csv"

# --- Constants ---
A0 = 1.2e-10  # m/s^2 (fixed SPARC value)

# --- Load data ---
df = pd.read_csv(RAR_FILE)

# Safety filter
df = df[(df["g_bar"] > 0) & (df["g_obs"] > 0)]

g_bar = df["g_bar"].values
g_obs = df["g_obs"].values

# --- Empirical RAR ---
g_rar = g_bar / (1.0 - np.exp(-np.sqrt(g_bar / A0)))

# --- Log residuals ---
log_residuals = np.log10(g_obs) - np.log10(g_rar)

# --- Scatter metrics ---
rms_scatter = np.sqrt(np.mean(log_residuals**2))
mad_scatter = np.median(np.abs(log_residuals))

print("-" * 50)
print("RAR Scatter Diagnostic (H1.5)")
print("-" * 50)
print(f"Total points analysed : {len(log_residuals)}")
print(f"RMS scatter (dex)      : {rms_scatter:.3f}")
print(f"Median |Δ| (dex)       : {mad_scatter:.3f}")
print("-" * 50)
