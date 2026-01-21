"""
H1.5 — RAR Assembly (with radial regimes)
Build Radial Acceleration Relation points from frozen H1 outputs.

Outputs:
- rar_points.csv with:
  name, g_bar, g_obs, r_frac
"""

import numpy as np
import pandas as pd
from pathlib import Path

# --- PATHS ---
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR   = SCRIPT_DIR.parent / "data" / "h1_frozen_results"
RC_DIR     = DATA_DIR / "per_galaxy"
OUT_FILE   = DATA_DIR / "rar_points.csv"

rows = []

for rc_file in sorted(RC_DIR.glob("rc_decomp_*_best.*")):
    name = rc_file.stem.replace("rc_decomp_", "").replace("_best", "")

    rc = pd.read_csv(rc_file)

    # Required columns
    required = {"R_kpc", "V_baryon", "V_total"}
    if not required.issubset(rc.columns):
        continue

    R = rc["R_kpc"].values
    Vb = rc["V_baryon"].values
    Vt = rc["V_total"].values

    # Normalize radius per galaxy
    R_max = np.max(R)
    if R_max <= 0:
        continue

    r_frac = R / R_max

    # Valid points
    mask = (R > 0) & (Vb > 0) & (Vt > 0)
    R = R[mask]
    Vb = Vb[mask]
    Vt = Vt[mask]
    r_frac = r_frac[mask]

    # Accelerations in natural units
    g_bar = (Vb**2) / R
    g_obs = (Vt**2) / R   # H1 prediction

    for gb, go, rf in zip(g_bar, g_obs, r_frac):
        if gb > 0 and go > 0:
            rows.append({
                "name": name,
                "g_bar": gb,
                "g_obs": go,
                "r_frac": rf
            })

df = pd.DataFrame(rows)
df.to_csv(OUT_FILE, index=False)

print("-" * 60)
print("RAR assembly complete (with radial fraction)")
print(f"Output file: {OUT_FILE}")
print(f"Total points: {len(df)}")
print("-" * 60)
