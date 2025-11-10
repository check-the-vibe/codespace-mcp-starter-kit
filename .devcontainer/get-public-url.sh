#!/bin/bash
# Wrapper to print public URL from devcontainer context
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ -f get-public-url.sh ]; then
  bash get-public-url.sh
else
  echo "Local endpoint: http://localhost:8000/mcp"
fi
