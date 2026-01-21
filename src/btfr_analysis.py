"""
H1.5 — BTFR Analysis
Step 1: Assemble BTFR table from frozen H1 outputs.
"""

import numpy as np
import pandas as pd
from pathlib import Path

# --- DIRECTORY ANCHORING ---
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "data" / "h1_frozen_results"

# THE FIX: Pointing to the specific subfolder identified by the sniffer
RC_DIR = DATA_DIR / "per_galaxy"

OUT_FILE = DATA_DIR / "btfr_table.csv"
SUMMARY_FILE = DATA_DIR / "fleet_summary_compact.csv"

if not RC_DIR.exists():
    print(f"ERROR: Could not find the galaxy directory at {RC_DIR}")
    exit(1)

print(f"Fractal Pilot: Synchronizing with {len(list(RC_DIR.glob('*')))} files in {RC_DIR}")

# Load fleet summary
fleet = pd.read_csv(SUMMARY_FILE)

btfr_rows = []

for _, row in fleet.iterrows():
    name = row["name"]
    
    # Check for both .csv and .dat to ensure no galaxy is left behind
    rc_file_csv = RC_DIR / f"rc_decomp_{name}_best.csv"
    rc_file_dat = RC_DIR / f"rc_decomp_{name}_best.dat"
    
    if rc_file_csv.exists():
        rc_file = rc_file_csv
    elif rc_file_dat.exists():
        rc_file = rc_file_dat
    else:
        # If the file isn't there, it might be an 'outlier' we need to note later
        continue

    # Load the data
    rc = pd.read_csv(rc_file)

    # Extract outer 20% of radii (The V_flat region)
    n = len(rc)
    if n < 5: continue
        
    outer = rc.iloc[int(0.8 * n):]

    # Calculate V_flat using the median of the total predicted velocity
    # This is the 'effective' flat velocity predicted by the H1 model
    V_flat = np.median(outer["V_total"].values)

    btfr_rows.append({
        "name": name,
        "M_b": np.nan,  # Placeholder for Step 2
        "V_flat": V_flat
    })

# Save the resulting table
btfr = pd.DataFrame(btfr_rows)
btfr.to_csv(OUT_FILE, index=False)

print("-" * 30)
print(f"SUCCESS: BTFR table created at {OUT_FILE}")
print(f"Galaxies successfully processed: {len(btfr)} / {len(fleet)}")
print("-" * 30)
