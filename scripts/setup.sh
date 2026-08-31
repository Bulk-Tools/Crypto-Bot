#!/usr/bin/env bash
set -euo pipefail

in_termux=false
if [ -n "${TERMUX_VERSION:-}" ]; then
  in_termux=true
elif [[ "${PREFIX:-}" == *"com.termux"* ]]; then
  in_termux=true
fi

if [ "$in_termux" = true ]; then
  pkg update -y
  pkg install -y python python-numpy clang libopenblas liblapack pkg-config python-cryptography libxml2 libxslt git
fi

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
python -m pip install --no-build-isolation -r requirements.txt || python -m pip install -r requirements.txt
python -m pip install --no-build-isolation -e . || python -m pip install -e .

mkdir -p data/raw data/processed data/parquet logs reports models
if [ ! -f .env ]; then
  cp .env.example .env
fi
chmod +x scripts/*.sh

python scripts/health_check.py || true
echo "Setup complete. Activate with: source .venv/bin/activate"
