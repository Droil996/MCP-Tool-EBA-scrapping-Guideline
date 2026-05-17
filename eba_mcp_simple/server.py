from __future__ import annotations

from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from eba_mcp_simple.mcp_instance import mcp

# Import necessari per registrare i decorator MCP:
# @mcp.tool(), @mcp.resource(), @mcp.prompt()
import eba_mcp_simple.mcp_tools
import eba_mcp_simple.mcp_resources
import eba_mcp_simple.mcp_prompt


# =============================================================================
# SERVER BOOTSTRAP
# =============================================================================
# Questo modulo espone l'applicazione MCP via HTTP.
# Non contiene tools, resources, prompts, modelli o logica applicativa.
# =============================================================================

@mcp.custom_route("/health", methods=["GET"])
async def health(request: Request) -> JSONResponse:
    return JSONResponse({"status": "ok", "server": "eba-regulatory-mcp-simple"})


def build_app():
    """Build and return the ASGI application."""
    app = mcp.http_app(path="/mcp", stateless_http=False)
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "mcp-session-id"],
        expose_headers=["mcp-session-id"],
    )
    return app
