# Causal Effects of Antibiotic Exposure on Antimicrobial Resistance

**A multi-site double machine learning study of 1.5 million culture episodes**

Aravind V. Kuruvikkattil, Shikhar Shukla, Leo A. Celi, Zanthia Wiley, Judy W. Gichoya, Saptarshi Purkayastha

This repository contains the analysis code for estimating the causal effect of prior antibiotic exposure on subsequent antimicrobial resistance using double machine learning (DML) with XGBoost GPU nuisance models across three U.S. health systems: Mass General Brigham (MGB), Stanford Health Care, and Beth Israel Deaconess Medical Center (BIDMC, via the MIMIC-IV dataset).

## Data Requirements

- **MGB**: [ARMD-MGB v1.0.0](https://physionet.org/content/armd-mgb/1.0.0/) (Wei & Kanjilal, 2025). Requires PhysioNet credentialed access.
- **Stanford**: [ARMD-Stanford](https://datadryad.org/dataset/doi:10.5061/dryad.jq2bvq8kp) (Nateghi Haredasht et al., 2025; Oct 22, 2025 release). Available on Dryad under CC0.
- **BIDMC/MIMIC**: [MIMIC-IV v3.1](https://physionet.org/content/mimiciv/3.1/) (Johnson et al., 2023). Requires CITI training and signed DUA.

Raw data files should be placed in:
- `/data0/armd/` (MGB)
- `/data0/armd-stanford/` (Stanford)
- `/data0/mimic-iv/` (BIDMC / MIMIC-IV)

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Requires Python 3.10+ and an NVIDIA GPU with CUDA support for XGBoost GPU acceleration.

## Usage

Run the full analysis pipeline:

```bash
./run_analysis.sh          # All 4 notebooks sequentially
./run_analysis.sh part1    # Data pipeline + primary DML only
./run_analysis.sh part2    # Sensitivity analyses only
./run_analysis.sh part3    # Cross-site downstream analyses only
./run_analysis.sh part4    # Empiric failure analysis only
```

Notebooks are executed via `jupyter nbconvert --execute` with a 2-hour timeout per notebook.
Total runtime: approximately 4-6 hours on a single GPU.

### Pipeline overview

| Step | Notebook | Description | Key outputs |
|------|----------|-------------|-------------|
| 1 | `01_data_pipeline_dml.ipynb` | Data build + primary DML | `*_dml_primary.csv`, `evalues.csv` |
| 2 | `02_sensitivity_analyses.ipynb` | IPTW robustness, E-values, window sensitivity, dose-response | `iptw_results.csv`, `dml_vs_iptw.csv` |
| 3 | `03_cross_site_downstream.ipynb` | Forest plot, heterogeneity, time decay, permutations, CEM | `fig1_forest_plot.pdf`, `fig_time_decay.pdf` |
| 4 | `04_empiric_failure_analysis.ipynb` | Empiric therapy failure rates and preventable failures | `ef_failure_all.csv`, failure figures |

Notebooks must be run in order (each depends on outputs from previous steps).

## Repository Structure

```
amr_causal/
├── README.md
├── LICENSE                            (MIT)
├── .gitignore
├── requirements.txt
├── run_analysis.sh                    (pipeline runner)
├── validate_pipeline.py               (output validation)
├── notebooks/
│   ├── 01_data_pipeline_dml.ipynb     (data build + primary DML)
│   ├── 02_sensitivity_analyses.ipynb  (IPTW, E-values, window, dose-response)
│   ├── 03_cross_site_downstream.ipynb (heterogeneity, permutations, CEM)
│   └── 04_empiric_failure_analysis.ipynb (empiric therapy failure)
├── outputs/
│   ├── data/                          (intermediate CSVs, gitignored)
│   ├── results/                       (analysis result CSVs)
│   └── figures/                       (publication figures)
├── manuscript/
│   ├── manuscript.tex
│   ├── supplementary.tex
│   └── figures/                       (copied from outputs/figures/)
└── executed/                          (executed notebooks, gitignored)
```

## Key Results

| Drug Class | MGB (ACE, pp) | Stanford (ACE, pp) | MIMIC-IV (ACE, pp) |
|------------|:-------------:|:------------------:|:------------------:|
| Fluoroquinolones | 14.8 | 16.5 | 8.7 |
| 3rd-gen cephalosporins | 5.6 | 8.7 | 3.6 |
| Carbapenems | 5.3 | 5.9 | 4.6 |
| Glycopeptides | 4.7 | 6.4 | 3.3 |
| Sulfonamides | 15.9 | 3.5* | --- |
| Ext-spec penicillins | 3.9 | 6.2 | 4.1 |
| Aminoglycosides | 3.4 | 7.4 | 6.7 |

All P < 0.005 except *P = 0.15. Sulfonamides not testable in MIMIC-IV.

## Citation

```bibtex
@article{kuruvikkattil2026amr,
  title   = {Prior Antibiotic Exposure and the Causal Risk of Antimicrobial Resistance: A Multi-Site Study of 1.5 Million Culture Episodes},
  author  = {Kuruvikkattil, Aravind V. and Shukla, Shikhar and Celi, Leo A. and Wiley, Zanthia and Gichoya, Judy W. and Purkayastha, Saptarshi},
  year    = {2026},
  journal = {Submitted},
}
```

## License

MIT License. See [LICENSE](LICENSE).
