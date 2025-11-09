from __future__ import annotations
import os
from typing import Any, Optional, List, Dict
from mcp.server.fastmcp import FastMCP

# The server created from this template should keep the same stack used in
# this repository: FastMCP for tool registration and a streamable-http
# Starlette app for HTTP integration.

HTTP_HOST = os.environ.get("MCP_HTTP_HOST", "0.0.0.0")
HTTP_PORT = int(os.environ.get("MCP_HTTP_PORT", "8000"))
HTTP_PATH = os.environ.get("MCP_HTTP_PATH", "/mcp")

# Create the FastMCP server. Change the name and other metadata for your project.
mcp = FastMCP("mcp-server-template", host=HTTP_HOST, port=HTTP_PORT, streamable_http_path=HTTP_PATH)


# Example placeholder tool: replace with real implementations.
@mcp.tool(title="Placeholder ping", description="A trivial ping tool used in the template.")
async def tool_ping(message: str = "hello") -> str:
    """Echo back the provided message.

    Replace this function with an actual tool for your server. Tools should
    be documented with clear parameter descriptions and return values.
    """
    return f"pong: {message}"


# Register additional placeholder tools here. For each tool, provide a clear
# docstring and examples. When creating a new MCP server from this template
# remove placeholder tools and implement project logic.


@mcp.tool(title="Health summary", description="Return a brief health summary string.")
async def tool_health_summary() -> str:
    # Keep this tiny tool for quick programmatic checks from MCP clients
    return "ok"


def main():
    # Default to stdio transport so the server can be launched by test harnesses
    # or run locally. In production you may use `mcp.run(transport='streamable-http')`
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
