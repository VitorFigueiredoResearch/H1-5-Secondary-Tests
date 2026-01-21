"""
H1.5 — BTFR Analysis
Step 2: Attach baryonic mass to H1-predicted V_flat.
"""

import pandas as pd
from pathlib import Path

# --- DIRECTORY ANCHORING ---
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "data" / "h1_frozen_results"

BTFR_FILE = DATA_DIR / "btfr_table.csv"
GALAXY_FILE = DATA_DIR / "galaxies.csv"
OUT_FILE = DATA_DIR / "btfr_table_with_mass.csv"

# Load tables
btfr = pd.read_csv(BTFR_FILE)
gal  = pd.read_csv(GALAXY_FILE)

# Compute baryonic mass (SPARC convention)
gal["M_b"] = gal["Mstar"] + 1.33 * gal["Mgas"]

# Keep only what we need
gal = gal[["name", "M_b"]]

# Merge with BTFR table
merged = btfr.merge(gal, on="name", how="inner")

# Save
merged.to_csv(OUT_FILE, index=False)

print("-" * 30)
print(f"SUCCESS: BTFR table with baryonic mass created at:")
print(OUT_FILE)
print(f"Galaxies included: {len(merged)} / {len(btfr)}")
print("-" * 30)
