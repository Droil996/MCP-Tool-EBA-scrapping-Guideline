"""Entry point for the simple EBA MCP server.

Usage:
    uv run eba-mcp-simple
    
"""
from __future__ import annotations

import logging
import os

import click


@click.command()
@click.option("--port", "-p", type=int, default=None, help="HTTP port (default: $MCP_PORT or 8001)")
@click.option("--host", "-H", type=str, default="0.0.0.0", help="Bind host")
@click.option("-v", "--verbose", count=True, help="Verbosity: -v INFO, -vv DEBUG")
def main(port: int | None, host: str, verbose: int) -> None:
    """Start the simple EBA MCP server."""
    level = {0: logging.WARNING, 1: logging.INFO}.get(verbose, logging.DEBUG)
    logging.basicConfig(level=level, format="%(levelname)s %(name)s: %(message)s")

    from dotenv import load_dotenv
    load_dotenv()

    import uvicorn
    from eba_mcp_simple.server import build_app

    effective_port = port or int(os.getenv("MCP_PORT", "8001"))
    app = build_app()

    click.echo(f"Starting simple EBA MCP server on http://{host}:{effective_port}/mcp")
    click.echo(f"Connect your MCP client to http://localhost:{effective_port}/mcp/")

    uvicorn.run(app, host=host, port=effective_port, access_log=False,)


if __name__ == "__main__":
    main()
