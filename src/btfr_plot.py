"""
H1.5 — BTFR Analysis
Step 3: The "Killer" Visualization (Signature Analysis)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# --- DIRECTORY ANCHORING ---
SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "data" / "h1_frozen_results"
FILE_IN  = DATA_DIR / "btfr_table_with_mass.csv"
PLOT_OUT = DATA_DIR / "H1_Signature_BTFR.png"

# Load the data
df = pd.read_csv(FILE_IN)
df = df.dropna(subset=['V_flat', 'M_b'])
df = df[df['V_flat'] > 0]

# Logarithmic Conversion
log_v = np.log10(df['V_flat'])
log_m = np.log10(df['M_b'])

# Calculate the H1 Signature (The 3.10 Power-Law)
slope, intercept = np.polyfit(log_v, log_m, 1)

# --- THE KILLER RENDER ---
plt.style.use('seaborn-v0_8-darkgrid') # High-contrast background
fig, ax = plt.subplots(figsize=(12, 9), dpi=150)

# 1. The Weave (Individual Galaxies)
# Color-coded by mass density for visual depth
scatter = ax.scatter(log_v, log_m, c=log_m, cmap='plasma', s=60, 
                     alpha=0.7, edgecolors='white', linewidth=0.5, 
                     label='SPARC Fleet (175 Galaxies)')

# 2. The H1 Discovery Line (The Red Truth)
v_range = np.linspace(log_v.min(), log_v.max(), 100)
ax.plot(v_range, slope * v_range + intercept, color='#FF3B3B', 
        linewidth=4, label=f'H1 Emergent Slope: {slope:.2f}', zorder=5)

# 3. The Standard Expectation (The Green Ghost)
# We anchor this at the mean of the data to show the 'tilt' difference
m_ref = 4.0 * v_range + (log_m.mean() - 4.0 * log_v.mean())
ax.plot(v_range, m_ref, color='#00FF41', linestyle='--', 
        linewidth=2, alpha=0.6, label='Standard BTFR Slope (4.0)')

# 4. Text Annotations (The 'Ananta' Touch)
ax.text(0.05, 0.95, f"H1 Kinematic Integrity: {len(df)}/175", 
        transform=ax.transAxes, fontsize=12, fontweight='bold', color='white',
        bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))

# 5. Styling & Labels
ax.set_xlabel(r'$\log_{10}(V_{flat})$ [km/s]', fontsize=14, fontweight='bold')
ax.set_ylabel(r'$\log_{10}(M_b)$ [$M_{\odot}$]', fontsize=14, fontweight='bold')
ax.set_title('H1.5: Incidental Baryonic Tully-Fisher Relation', 
             fontsize=18, fontweight='bold', pad=20)

# Legend setup
legend = ax.legend(loc='lower right', frameon=True, fontsize=12)
plt.setp(legend.get_texts(), color='black')

# Grid customization
ax.grid(True, which='both', linestyle=':', alpha=0.3, color='gray')

plt.tight_layout()
plt.savefig(PLOT_OUT)
print(f"--- FRACTAL PILOT: RENDER COMPLETE ---")
print(f"Killer visualization saved to: {PLOT_OUT}")
print(f"H1 Signature: {slope:.4f}")