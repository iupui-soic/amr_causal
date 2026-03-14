# Causal Effects of Antibiotic Exposure on Antimicrobial Resistance

**A multi-site double machine learning study of 1.5 million culture episodes**

This repository contains the analysis code for estimating the causal effect of prior antibiotic exposure on subsequent antimicrobial resistance using double machine learning (DML) with XGBoost GPU nuisance models across three U.S. health systems: Mass General Brigham (MGB), Stanford Health Care, and Beth Israel Deaconess Medical Center (BIDMC, via the MIMIC-IV dataset).

## Data Requirements

- **MGB and Stanford**: Antimicrobial Resistance and Microbiome Database (ARMD) v1.0.0. Access requires institutional data use agreement.
- **MIMIC-IV v3.1**: Publicly available via [PhysioNet](https://physionet.org/content/mimiciv/3.1/). Requires CITI training and signed DUA.

Raw data files should be placed in:
- `/data0/armd/` (MGB)
- `/data0/armd-stanford/` (Stanford)
- `/data0/mimic-iv/` (MIMIC-IV)

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
./run_analysis.sh          # All 3 notebooks sequentially
./run_analysis.sh part1    # Data pipeline + primary DML only
./run_analysis.sh part2    # Sensitivity analyses only
./run_analysis.sh final    # Cross-site analyses only
```

Total runtime: approximately 3-5 hours on a single GPU.

## Repository Structure

```
amr_causal/
├── README.md
├── LICENSE                            (MIT)
├── .gitignore
├── requirements.txt
├── run_analysis.sh                    (pipeline runner)
├── notebooks/
│   ├── 01_data_pipeline_dml.ipynb     (data build + primary DML)
│   ├── 02_sensitivity_analyses.ipynb  (IPTW, E-values, window, dose-response)
│   └── 03_cross_site_analyses.ipynb   (heterogeneity, permutations, CEM)
├── outputs/
│   ├── data/                          (intermediate CSVs, gitignored)
│   ├── results/                       (analysis result CSVs)
│   └── figures/                       (publication figures)
└── executed/                          (executed notebooks, gitignored)
```

## Key Results

| Drug Class | MGB (ACE, pp) | Stanford (ACE, pp) | MIMIC-IV (ACE, pp) |
|------------|:-------------:|:------------------:|:------------------:|
| Fluoroquinolones | 14.8 | 16.8 | 8.7 |
| 3rd-gen cephalosporins | 5.6 | 8.4 | 3.6 |
| Carbapenems | 5.3 | 5.8 | 4.6 |
| Glycopeptides | 4.7 | 6.2 | 3.3 |
| Sulfonamides | 15.8 | 3.9* | --- |
| Ext-spec penicillins | 3.9 | 6.0 | 4.1 |
| Aminoglycosides | 3.3 | 7.5 | 6.7 |

All P < 0.005 except *P = 0.16. Sulfonamides not testable in MIMIC-IV.

## Citation

```bibtex
@article{kuruvikkattil2026amr,
  title   = {Prior Antibiotic Exposure and the Causal Risk of
             Antimicrobial Resistance: A Multi-Site Study of
             1.5 Million Culture Episodes},
  author  = {Kuruvikkattil, Aravind V. and others},
  year    = {2026},
  journal = {Submitted},
}
```

## License

MIT License. See [LICENSE](LICENSE).
