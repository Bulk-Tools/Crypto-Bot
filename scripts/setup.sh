#!/usr/bin/env bash
set -euo pipefail

if ! command -v python >/dev/null 2>&1; then
  echo "Python is required. Install python in Termux first."
  exit 1
fi
if ! command -v git >/dev/null 2>&1; then
  echo "Git is required. Install git in Termux first."
  exit 1
fi

if [ ! -d .venv ]; then
  python -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

mkdir -p data/raw data/processed data/parquet logs reports models
if [ ! -f .env ]; then
  cp .env.example .env
fi

python scripts/health_check.py || true
echo "Setup complete. Activate with: source .venv/bin/activate"
