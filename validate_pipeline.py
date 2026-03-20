#!/home/saptpurk/amr_causal/.venv/bin/python
"""
Validate pipeline outputs after running all 4 notebooks.
Checks master data files, result CSVs, and figures.
Exit code 0 = all checks pass, 1 = failure.

Usage:
    python3 validate_pipeline.py
"""
import sys
import os
import pandas as pd

BASE_DATA = 'outputs/data/'
BASE_RESULTS = 'outputs/results/'
BASE_FIGURES = 'outputs/figures/'
FAILURES = []


def check(condition, msg):
    if not condition:
        FAILURES.append(msg)
        print(f'  FAIL: {msg}')
    else:
        print(f'  OK:   {msg}')


def validate_master_data():
    """Check that master data files exist and have correct structure."""
    print('\n── Master Data Files')
    for name, path in [
        ('MGB', BASE_DATA + 'mgb/mgb_master_v3.csv'),
        ('Stanford', BASE_DATA + 'stanford/stanford_master_v2.csv'),
        ('MIMIC', BASE_DATA + 'mimic/mimic_master_v3.csv'),
    ]:
        if not os.path.exists(path):
            FAILURES.append(f'{name} master file not found: {path}')
            print(f'  FAIL: {name} not found')
            continue
        df = pd.read_csv(path, nrows=5, low_memory=False)
        check(len(df) > 0, f'{name} master file exists and is non-empty')


def validate_dml_results():
    """Check primary DML result CSVs."""
    print('\n── Primary DML Results')
    expected = {
        'mgb_dml_primary.csv': 7,
        'stanford_dml_primary.csv': 7,
        'mimic_dml_primary.csv': 6,  # no Sulfa
    }
    for fname, expected_rows in expected.items():
        path = BASE_RESULTS + fname
        if not os.path.exists(path):
            FAILURES.append(f'DML result not found: {fname}')
            print(f'  FAIL: {fname} not found')
            continue
        df = pd.read_csv(path)
        check(len(df) == expected_rows,
              f'{fname}: {len(df)} rows (expected {expected_rows})')
        check('theta_pp' in df.columns, f'{fname}: has theta_pp column')


def validate_sensitivity_results():
    """Check sensitivity analysis CSVs."""
    print('\n── Sensitivity Analysis Results')
    required_csvs = [
        'iptw_results.csv',
        'dml_vs_iptw.csv',
        'evalues.csv',
        'evalue_sensitivity.csv',
        'time_decay_results.csv',
    ]
    for fname in required_csvs:
        path = BASE_RESULTS + fname
        check(os.path.exists(path), f'{fname} exists')


def validate_empiric_failure():
    """Check empiric failure analysis outputs."""
    print('\n── Empiric Failure Results')
    required = [
        'ef_failure_all.csv',
        'ef_failure_blood.csv',
        'ef_policy_all.csv',
    ]
    for fname in required:
        path = BASE_RESULTS + fname
        check(os.path.exists(path), f'{fname} exists')


def validate_figures():
    """Check that key figures were generated."""
    print('\n── Figures')
    required_figs = [
        'fig1_forest_plot.pdf',
        'fig_evalues.pdf',
        'fig_time_decay.pdf',
        'fig_dml_vs_iptw.pdf',
        'ef_fig1_blood_failure_forest.pdf',
    ]
    for fname in required_figs:
        path = BASE_FIGURES + fname
        check(os.path.exists(path), f'{fname} exists')


def validate_manuscript_consistency():
    """Spot-check that manuscript Table 2 FQ values match DML CSVs."""
    print('\n── Manuscript Consistency (spot check)')
    tex_path = 'manuscript/manuscript.tex'
    if not os.path.exists(tex_path):
        print('  SKIP: manuscript.tex not found')
        return

    mgb_path = BASE_RESULTS + 'mgb_dml_primary.csv'
    if not os.path.exists(mgb_path):
        print('  SKIP: mgb_dml_primary.csv not found')
        return

    mgb = pd.read_csv(mgb_path)
    fq = mgb[mgb['label'] == 'FQ'].iloc[0]
    fq_ace = round(fq['theta_pp'], 1)

    with open(tex_path) as f:
        tex = f.read()

    # Check that the FQ ACE appears in the manuscript
    check(str(fq_ace) in tex,
          f'MGB FQ ACE ({fq_ace}) found in manuscript.tex')


if __name__ == '__main__':
    print('=' * 60)
    print('PIPELINE VALIDATION')
    print('=' * 60)

    validate_master_data()
    validate_dml_results()
    validate_sensitivity_results()
    validate_empiric_failure()
    validate_figures()
    validate_manuscript_consistency()

    print('\n' + '=' * 60)
    if FAILURES:
        print(f'FAILED — {len(FAILURES)} issue(s):')
        for f in FAILURES:
            print(f'  - {f}')
        sys.exit(1)
    else:
        print('ALL CHECKS PASSED')
        sys.exit(0)
