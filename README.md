[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18321595.svg)](https://doi.org/10.5281/zenodo.18321595)

# H1.5 — Secondary Diagnostic Tests

This repository contains the full analysis pipeline and results for **H1.5**, a diagnostic study evaluating the frozen H1 baryon-convolved potential model against two empirical scaling relations:

- The Baryonic Tully–Fisher Relation (BTFR)
- The Radial Acceleration Relation (RAR)

## Scope
H1.5 is a **diagnostic-only study**.  
No model parameters are modified, optimised, or re-fitted.

## Relation to H1
- H1 is treated as a **frozen input**
- All rotation curve outputs are precomputed
- This repository performs *secondary analysis only*

H1 (frozen model): DOI: 10.5281/zenodo.18065273

To reproduce results, create the environment with:
conda env create -f environment.yml

## Contents
- `scripts/` — analysis and plotting scripts
- `data/` — derived diagnostic tables
- `figures/` — figures used in the manuscript
- `paper/` — LaTeX source for the H1.5 manuscript

## Reproducibility
All results can be reproduced using the scripts provided.  
No random seeds or per-galaxy tuning are employed.

## License
MIT
### Related Releases

**H1 (Frozen Model):** https://doi.org/10.5281/zenodo.18065273  
**H1.5 (Diagnostic Tests):** https://doi.org/10.5281/zenodo.18321595

## Citation

If you use this work, please cite:

**H1.5 — Diagnostic Tests of a Frozen Nonlocal Baryonic Model Against the BTFR and RAR**  
Zenodo (2025).  

H1.5 is a diagnostic analysis of the frozen H1 model.
The manuscript was submitted to MNRAS and received a desk rejection.
The present version reflects post-submission clarification and correction only.
No numerical results have been altered.
