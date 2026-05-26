#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

mkdir -p data/raw data/processed data/sample_cases screenshots animations

echo ""
echo "Setup complete."
echo ""
echo "Run the portable demo:"
echo "  source .venv/bin/activate"
echo "  python scripts/setup_case.py"
echo "  python scripts/export_visuals.py --input data/processed/sample_car_flow.vtu"
echo "  python scripts/create_streamlines.py --input data/processed/sample_car_flow.vtu"
echo "  python scripts/generate_animation.py --input data/processed/sample_car_flow.vtu --format gif"
echo "  python scripts/metrics_analysis.py --input data/processed/metrics.csv"
