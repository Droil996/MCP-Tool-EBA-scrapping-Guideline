from fastmcp import FastMCP


# =============================================================================
# MCP INSTANCE
# =============================================================================
# Questo modulo crea l'istanza condivisa FastMCP usata da:
# - tools
# - resources
# - prompts
# - server
#
# =============================================================================

mcp = FastMCP(
    name="eba-regulatory-mcp-simple",
    instructions=(
        "Server MCP didattico per monitorare pubblicazioni EBA e classificarne "
        "l'impatto regolamentare in Alto, Medio o Basso."
    ),
)
