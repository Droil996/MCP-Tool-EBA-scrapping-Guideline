from __future__ import annotations

from eba_mcp_simple.mcp_instance import mcp

# =============================================================================
# MCP RESOURCES
# =============================================================================
# Le Resources MCP sono dati contestuali controllati dall'applicazione client.
# In questo progetto forniscono all'Agent:
# - tassonomia regolamentare EBA
# - regole di classificazione Alto / Medio / Basso
# =============================================================================


@mcp.resource(
    "eba://taxonomy",
    title="EBA Regulatory Taxonomy",
)
def eba_taxonomy() -> str:
    return """
Aree tematiche EBA:

1. Governance
2. AML / Compliance
3. Capital Requirements
4. Regulatory Reporting
5. ESG
6. ICT / DORA
7. Consumer Protection
8. Supervisory Review
""".strip()
@mcp.resource(
    "eba://classification/rules",
    title="EBA Impact Classification Rules",
)
def classification_rules() -> str:
    return """
Classificazione impatto EBA:

ALTO / ROSSO:
- Final Guidelines
- RTS / ITS
- obblighi regolamentari
- impatti operativi
- reporting
- capitale
- compliance
- governance

MEDIO / GIALLO:
- Consultation Paper
- Draft document
- Opinion
- Report
- monitoraggio richiesto

BASSO / VERDE:
- Speech
- Newsletter
- materiale informativo

Confidence:
- Alta
- Media
- Bassa
""".strip()