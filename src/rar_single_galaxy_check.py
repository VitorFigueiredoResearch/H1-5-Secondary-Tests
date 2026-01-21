"""
H1.5 — Single Galaxy RAR Sanity Check

Purpose:
--------
Verify RAR quantities (g_bar, g_obs) for a single galaxy
directly from frozen H1 per-galaxy rotation curve outputs.

This script is intended for:
- independent verification
- referee sanity checks
- future reproducibility

Author: Vítor M. F. Figueiredo
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ==========================================================
# USER SETTINGS
# ==========================================================

TARGET_GALAXY = "NGC3198"   # change freely
MAX_ROWS = 10              # number of rows to display

# ==========================================================
# PATHS (do not edit unless repo structure changes)
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "h1_frozen_results"

RAR_FILE = DATA_DIR / "rar_points.csv"
RC_FILE  = DATA_DIR / "per_galaxy" / f"rc_decomp_{TARGET_GALAXY}_best.csv"

# ==========================================================
# LOAD DATA
# ==========================================================

if not RAR_FILE.exists():
    raise FileNotFoundError(f"Missing RAR file: {RAR_FILE}")

if not RC_FILE.exists():
    raise FileNotFoundError(f"Missing RC file for {TARGET_GALAXY}: {RC_FILE}")

rar = pd.read_csv(RAR_FILE)
rc  = pd.read_csv(RC_FILE)

# ==========================================================
# FILTER TARGET GALAXY
# ==========================================================

rar_gal = rar[rar["name"] == TARGET_GALAXY].copy()

if len(rar_gal) == 0:
    raise ValueError(f"No RAR points found for galaxy: {TARGET_GALAXY}")

# ==========================================================
# RECOMPUTE ACCELERATIONS FROM RC FILE
# ==========================================================

R  = rc["R_kpc"].values
Vb = rc["V_baryon"].values
Vt = rc["V_total"].values

mask = (R > 0) & (Vb > 0) & (Vt > 0)

R  = R[mask]
Vb = Vb[mask]
Vt = Vt[mask]

g_bar_check = (Vb**2) / R
g_obs_check = (Vt**2) / R

# ==========================================================
# OUTPUT
# ==========================================================

print("=" * 72)
print(f"H1.5 — RAR Single-Galaxy Verification")
print(f"Galaxy: {TARGET_GALAXY}")
print("=" * 72)

print("\nFirst rows from rar_points.csv:")
print(rar_gal[["g_bar", "g_obs", "r_frac"]].head(MAX_ROWS))

print("\nRecomputed from rc_decomp file:")
for i in range(min(MAX_ROWS, len(R))):
    print(
        f"R={R[i]:6.3f} kpc | "
        f"g_bar={g_bar_check[i]:12.6f} | "
        f"g_obs={g_obs_check[i]:12.6f}"
    )

# ==========================================================
# NUMERICAL CONSISTENCY CHECK
# ==========================================================

# Align lengths conservatively
n = min(len(rar_gal), len(g_bar_check))

delta_bar = np.abs(rar_gal["g_bar"].values[:n] - g_bar_check[:n])
delta_obs = np.abs(rar_gal["g_obs"].values[:n] - g_obs_check[:n])

print("\nConsistency check (absolute differences):")
print(f"max |Δ g_bar| = {delta_bar.max():.6e}")
print(f"max |Δ g_obs| = {delta_obs.max():.6e}")

if delta_bar.max() < 1e-10 and delta_obs.max() < 1e-10:
    print("\nSTATUS: ✅ Perfect numerical agreement")
else:
    print("\nSTATUS: ⚠ Differences detected (inspect values)")

print("=" * 72)
