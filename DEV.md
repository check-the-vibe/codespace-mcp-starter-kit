# Developing an MCP Server from the Template

This `mcp-server-template` directory provides a minimal, Codespaces-friendly
starter for building new MCP servers. It uses the same stack as the
`mcp-content-library` project (FastMCP + Starlette streamable-http app).

The goal is to provide a reproducible, easy-to-fill template so new servers
have a consistent structure, sensible defaults for Codespaces, and a clear
developer guide explaining the important areas to implement.

## Key files

- `app.py` — Starlette app instance that mounts the MCP streamable-http app,
  provides a small landing page and a `/health` endpoint. Keep `get_public_url()`
  to preserve Codespaces/Gitpod-friendly links.
- `server.py` — Creates the `FastMCP` instance and registers tools. Replace
  placeholder tools with the business logic for your server.
- `server_http.py` — Simple runner that launches the Starlette ASGI app with
  `uvicorn` or falls back to `mcp.run(...)` if necessary.

## Development workflow (Codespaces)

1. Open the repository in GitHub Codespaces.
2. Install Python deps in the Codespace (the repo root `requirements.txt` is
   the starting point):

```bash
pip install -r requirements.txt
```

3. Run the template server locally in the Codespace:

```bash
python mcp-server-template/server_http.py
```

4. Forward the port (Codespaces does this automatically for the default
   `8000` port). Use the `get_public_url()` helper to find the public URL.

## What to implement when creating a real server

1. Tools (in `server.py`):
   - Replace placeholder functions with well-documented tools using
     `@mcp.tool(...)` decorators. Each tool should have a clear docstring,
     inputs, outputs, and an example. Keep tools small and single-purpose.
2. Storage & nodes: decide how you will persist nodes (files, DB). The
   template is storage-agnostic; consider copying patterns from
   `mcp-content-library/storage.py` if you want a filesystem-backed approach.
3. Search & indexing: include logic to index content if full-text search is
   needed (see `search.py` in the example project for a small TF-IDF index).
4. Security & CORS: the template allows CORS from everywhere for convenience.
   Lock this down in production.
5. Health & diagnostics: extend `/health` to include dependency checks
   (database connectivity, index last-updated timestamp, disk space, etc.).
6. Tests: add unit tests and a basic end-to-end test similar to
   `test_basic.py` to validate core flows without running the HTTP server.

## Environment variables

- `MCP_HTTP_HOST` — host to bind (default `0.0.0.0`)
- `MCP_HTTP_PORT` — port to bind (default `8000`)
- `MCP_HTTP_PATH` — streamable-http path for MCP (default `/mcp`)
- `MCP_SNIPPETS_ROOT` — optional storage root (if using filesystem storage)

## Tips for Codespaces integration

- Keep the default port at `8000`. Codespaces will automatically expose this
  port and populate `CODESPACE_NAME` and `GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN`.
- Use `get_public_url()` from `app.py` to construct links that will work both
  locally and in Codespaces.

## Running with Docker (recommended for template)

The template is Docker-first so it will run the same inside Codespaces or on
your machine. By default it mounts `./data` into the container at `/data`
which becomes the `MCP_SNIPPETS_ROOT`.

Quick docker-compose start (from `mcp-server-template`):

```bash
docker compose up --build -d
```

Stop and remove the container:

```bash
docker compose down
```

The container exposes port 8000 which Codespaces maps to a public URL. The
template defaults to storing data on the host in `mcp-server-template/data`.

## Next steps

- Replace the placeholder tools with your server-specific implementations.
- Add a `README.md` and metadata describing the purpose of the new server.
- Add CI checks that run the template's tests and a quick syntax check.

If you'd like, I can:
- Replace the placeholder tools now with a small real example (e.g., a
  DB-backed counter), or
- Wire up a simple filesystem-based storage (like the example project) so
  the template is fully runnable out of the box.
