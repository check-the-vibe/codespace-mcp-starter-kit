#!/usr/bin/env bash
set -euo pipefail

echo "[postStart] devcontainer postStart wrapper (repo-root version)"

# When placed in repo root, ROOT_DIR is the script's directory (should be repo root)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

# Non-interactive bootstrap (creates .venv and installs deps)
if [ -f "./bootstrap.sh" ]; then
  echo "[postStart] Running bootstrap (non-interactive)"
  bash ./bootstrap.sh --non-interactive || true
fi

# Activate venv if present
if [ -f ".venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

# Start server in background if not already running
PID_FILE="/tmp/mcp_server.pid"
LOG_FILE="/tmp/mcp_server.log"

is_running() {
  if [ -f "$PID_FILE" ]; then
    pid=$(cat "$PID_FILE")
    if kill -0 "$pid" 2>/dev/null; then
      return 0
    else
      return 1
    fi
  fi
  return 1
}

if is_running; then
  echo "[postStart] MCP server already running (pid $(cat "$PID_FILE"))"
  exit 0
fi

HOST="${MCP_HTTP_HOST:-0.0.0.0}"
PORT="${MCP_HTTP_PORT:-8000}"

echo "[postStart] Starting MCP server on $HOST:$PORT"

nohup "${ROOT_DIR}/.venv/bin/python" "${ROOT_DIR}/server_http.py" > "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"

echo "[postStart] MCP server started (pid $(cat "$PID_FILE")); logs: $LOG_FILE"

# Wait for server to be healthy before making port public
echo "[postStart] Waiting for server to be ready..."
MAX_ATTEMPTS=30
ATTEMPT=0
while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
  if curl -fsS "http://localhost:$PORT/health" > /dev/null 2>&1; then
    echo "[postStart] ✓ Server is healthy!"
    break
  fi
  ATTEMPT=$((ATTEMPT + 1))
  echo "[postStart] Health check attempt $ATTEMPT/$MAX_ATTEMPTS..."
  sleep 1
done

if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
  echo "[postStart] ⚠ Server health check timeout after ${MAX_ATTEMPTS}s"
else
  echo "[postStart] ✓ Server is ready and accessible at http://0.0.0.0:$PORT"
fi

exit 0
