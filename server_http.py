"""Lightweight HTTP runner for the template MCP server.

This mirrors the pattern used by the example project: it tries to import
the Starlette `app` from `app.py` and run it with `uvicorn`. If that fails,
it falls back to calling `mcp.run(...)` from `server.py`.
"""
import os
import traceback

try:
    from app import app  # the Starlette app instance
    has_app = True
except Exception:
    has_app = False

try:
    import uvicorn  # type: ignore
    has_uvicorn = True
except Exception:
    has_uvicorn = False


def _run_uvicorn():
    host = os.environ.get("MCP_HTTP_HOST", "0.0.0.0")
    port = int(os.environ.get("MCP_HTTP_PORT", "8000"))
    if has_app and has_uvicorn:
        uvicorn.run(app, host=host, port=port, log_level="info")
    elif has_app and not has_uvicorn:
        print("uvicorn is not installed. Install requirements: pip install -r requirements.txt")
        raise RuntimeError("uvicorn not available")
    else:
        raise RuntimeError("ASGI app not available (app.py missing or import failed)")


if __name__ == "__main__":
    try:
        _run_uvicorn()
    except Exception:
        print("Failed to start uvicorn/app — falling back to mcp.run if available.\n")
        traceback.print_exc()
        try:
            from server import mcp

            print("Attempting fallback: mcp.run(transport='streamable-http')")
            mcp.run(transport="streamable-http")
        except Exception:
            print("Fallback failed. Please ensure uvicorn is installed and app.py is present.")
            traceback.print_exc()
            raise
