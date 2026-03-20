#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════
# AMR Causal Analysis — Full Pipeline Runner
# ══════════════════════════════════════════════════════════════
#
# Usage:
#   ./run_analysis.sh              # Run all 4 notebooks in order
#   ./run_analysis.sh part1        # Data pipeline + primary DML
#   ./run_analysis.sh part2        # Sensitivity analyses (IPTW, E-values)
#   ./run_analysis.sh part3        # Cross-site downstream analyses
#   ./run_analysis.sh part4        # Empiric failure analysis
#
# Prerequisites:
#   python3 -m venv .venv
#   source .venv/bin/activate
#   pip install -r requirements.txt
#
# Output structure:
#   outputs/
#     data/mgb/          — MGB intermediate master CSVs
#     data/stanford/     — Stanford intermediate master CSVs
#     data/mimic/        — MIMIC intermediate master CSVs
#     results/           — All analysis result CSVs
#     figures/           — All PDF/PNG figures
# ══════════════════════════════════════════════════════════════

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Activate venv
if [ -f .venv/bin/activate ]; then
    source .venv/bin/activate
else
    echo "ERROR: .venv not found. Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Create output directories
mkdir -p outputs/{data/{mgb,stanford,mimic,validation},results,figures}

EXECUTED_DIR="$SCRIPT_DIR/executed"
mkdir -p "$EXECUTED_DIR"

run_notebook() {
    local input="notebooks/$1"
    local basename="${1%.ipynb}"
    local output="$EXECUTED_DIR/${basename}_executed.ipynb"
    echo ""
    echo "══════════════════════════════════════════════════════════════"
    echo "  Running: $input"
    echo "  Output:  $output"
    echo "  Started: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "══════════════════════════════════════════════════════════════"
    jupyter nbconvert --to notebook --execute "$input" \
        --output "$(realpath "$output")" \
        --ExecutePreprocessor.timeout=7200 \
        --ExecutePreprocessor.kernel_name=python3
    echo "  Finished: $(date '+%Y-%m-%d %H:%M:%S')"
    echo "  Status:   SUCCESS"
}

TARGET="${1:-all}"

case "$TARGET" in
    part1)
        run_notebook 01_data_pipeline_dml.ipynb
        ;;
    part2)
        run_notebook 02_sensitivity_analyses.ipynb
        ;;
    part3)
        run_notebook 03_cross_site_downstream.ipynb
        ;;
    part4)
        run_notebook 04_empiric_failure_analysis.ipynb
        ;;
    all)
        run_notebook 01_data_pipeline_dml.ipynb
        run_notebook 02_sensitivity_analyses.ipynb
        run_notebook 03_cross_site_downstream.ipynb
        run_notebook 04_empiric_failure_analysis.ipynb

        # Copy figures to manuscript directory
        echo ""
        echo "  Copying figures to manuscript/figures/ ..."
        mkdir -p manuscript/figures/png
        cp outputs/figures/*.pdf manuscript/figures/ 2>/dev/null || true
        cp outputs/figures/*.png manuscript/figures/png/ 2>/dev/null || true

        echo ""
        echo "══════════════════════════════════════════════════════════════"
        echo "  ALL 4 NOTEBOOKS COMPLETED SUCCESSFULLY"
        echo "  Results: outputs/results/"
        echo "  Figures: outputs/figures/"
        echo "══════════════════════════════════════════════════════════════"
        ;;
    *)
        echo "Usage: $0 [part1|part2|part3|part4|all]"
        exit 1
        ;;
esac
