import os
from datetime import datetime
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from server import mcp

# Use the MCP-provided Starlette app so streamable-http is initialized
app = mcp.streamable_http_app()

# CORS: permissive for development; tune for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Mcp-Session-Id"],
)


def get_public_url():
    """Return a public-facing URL for Codespaces/Gitpod or localhost.

    This helper is useful in developer environments to build links that
    work when running inside GitHub Codespaces. Keep this in the template
    so developers don't need to think about it when creating a new server.
    """
    codespace_name = os.environ.get("CODESPACE_NAME")
    port_forwarding_domain = os.environ.get("GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN")
    if codespace_name and port_forwarding_domain:
        return f"https://{codespace_name}-8000.{port_forwarding_domain}"

    gitpod_workspace_url = os.environ.get("GITPOD_WORKSPACE_URL")
    if gitpod_workspace_url:
        workspace_url = gitpod_workspace_url.replace("https://", "")
        return f"https://8000-{workspace_url}"

    return "http://localhost:8000"


async def homepage(request):
    """Simple landing page for the template server.

    Replace this with project-specific UI or delete it when creating a
    new MCP server from the template.
    """
    base_url = get_public_url()
    mcp_endpoint = f"{base_url}/mcp"
    html = f"""
    <!doctype html>
    <html>
      <head><meta charset="utf-8"><title>MCP Server Template</title></head>
      <body>
        <h1>MCP Server Template</h1>
        <p>This is a minimal MCP server template. Replace the placeholder
        tools and handlers with your project's logic.</p>
        <ul>
          <li><strong>MCP endpoint</strong>: <a href="{mcp_endpoint}">{mcp_endpoint}</a></li>
          <li><strong>Health</strong>: <a href="/health">/health</a></li>
        </ul>
      </body>
    </html>
    """
    return HTMLResponse(content=html)


async def health_check(request):
    """Return a minimal health JSON response.

    Developers can extend this to include dependency checks, DB status,
    index health, etc.
    """
    return JSONResponse({
        "status": "healthy",
        "service": "mcp-server-template",
        "timestamp": datetime.utcnow().isoformat(),
        "mcp_endpoint": f"{get_public_url()}/mcp",
    })


# Register routes
app.add_route("/", homepage, methods=["GET"])
app.add_route("/health", health_check, methods=["GET"])
