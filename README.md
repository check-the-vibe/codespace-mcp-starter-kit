# MCP Server Template

This directory is a minimal template for creating a new MCP server.
It is intentionally small and Docker-first so you can get a running
instance quickly. Storage is filesystem-backed by default and persists
to `./mcp-server-template/data` when running with Docker Compose.

Key features:
- FastMCP-based tool registration (`server.py`)
- Starlette ASGI app (`app.py`) with Codespaces-friendly `get_public_url()`
- Minimal filesystem storage (writes nodes to `/data` inside the container)
- Dockerfile and docker-compose for quick startup

Quick start (from repo root):

```bash
# Build and run with docker-compose
cd mcp-server-template
docker compose up --build -d

# Visit the app (Codespaces will expose it automatically) or
# on local machine: http://localhost:8000/
```

Storage location on the host after running docker-compose:

```
mcp-server-template/data/nodes/content/*.json
```

If you prefer to run without Docker, install the project requirements and run:

```bash
pip install -r requirements.txt
python mcp-server-template/server_http.py
```

Next steps:
- Replace placeholder tools in `server.py` with project logic.
- Extend `storage.py` or swap in the repository's `storage.py` if you want
  the fuller feature set (tags, links, edges, indexing).
- Update `DEV.md` with project-specific development notes.
