#!/bin/bash
# Copied interactive setup into .devcontainer for template cleanliness
set -euo pipefail

# shellcheck disable=SC1091
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ -f "setup-claude-cli.sh" ]; then
  bash setup-claude-cli.sh
else
  echo "No setup-claude-cli.sh found in project root; creating basic .claude config"
  mkdir -p .claude
  cat > .claude/mcp_config.json << 'EOF'
{
  "mcpServers": {
    "content-library": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
EOF
  echo "Created .claude/mcp_config.json"
fi
