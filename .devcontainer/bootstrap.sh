#!/bin/bash
# Unified bootstrap script for MCP Server template (devcontainer)
# Sets up virtualenv and installs Python dependencies (non-interactive by default)

set -euo pipefail

NON_INTERACTIVE=false
SKIP_CLI_INSTALL=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --non-interactive|-n)
      NON_INTERACTIVE=true; shift;;
    --skip-cli)
      SKIP_CLI_INSTALL=true; shift;;
    --help|-h)
      echo "Usage: ./bootstrap.sh [--non-interactive]"; exit 0;;
    *) echo "Unknown option: $1"; exit 1;;
  esac
done

echo "[bootstrap] Creating/activating virtualenv and installing dependencies"

if [ -d ".venv" ]; then
  echo "[bootstrap] .venv already exists"
else
  python3 -m venv .venv
  echo "[bootstrap] virtualenv created"
fi

# shellcheck disable=SC1091
source .venv/bin/activate

pip install -q --upgrade pip
pip install -q -e . || true
if [ -f requirements.txt ]; then
  pip install -q -r requirements.txt || true
fi

echo "[bootstrap] Dependencies installed (best-effort)"

if [ "$NON_INTERACTIVE" = false ]; then
  echo "Bootstrap completed. You can start the HTTP server with: ./start.sh"
else
  echo "Bootstrap completed (non-interactive)."
fi

exit 0
