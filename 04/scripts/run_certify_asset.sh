#!/usr/bin/env bash
# certify_asset.py — launcher for macOS / Linux
# Usage: ./run_certify_asset.sh <file>  [--author "Name"] [--notes "..."]
#        ./run_certify_asset.sh <file>  --verify

cd "$(dirname "$0")"

PY=""
for v in python3.13 python3.12 python3.11 python3.10 python3.9 python3 python; do
    if command -v "$v" &>/dev/null; then PY="$v"; break; fi
done

if [ -z "$PY" ]; then
    echo "[ERROR] Python not found. Install Python 3.x."
    exit 1
fi

echo "[certify_asset] Using: $($PY --version)"
echo ""

if [ -z "$1" ]; then
    echo "Usage: ./run_certify_asset.sh <file> [--author \"Name\"] [--notes \"...\"]"
    echo "       ./run_certify_asset.sh <file> --verify"
else
    "$PY" certify_asset.py "$@"
fi
