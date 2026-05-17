from __future__ import annotations


# =============================================================================
# MCP PROMPTS
# =============================================================================
# I Prompts MCP sono template controllati dall'utente.
# Vengono invocati tramite per guidare l'Agent/LLM nell'analisi regolamentare.
# =============================================================================

from eba_mcp_simple.mcp_instance import mcp

@mcp.prompt()
def analizza_guideline(
    title: str,
    preview_text: str,
    pdf_path: str = "",
    source_url: str = "",
) -> str:

    return f"""

Sei un regulatory analyst esperto di normativa bancaria europea.

Usa:
- eba://classification/rules
- eba://taxonomy

per analizzare questa Guideline EBA.

Titolo:
{title}

PDF:
{pdf_path}

Fonte:
{source_url}

Preview:
{preview_text[:3000]}

Restituisci SOLO un JSON valido:

{{
  "title": "...",
  "relevance_score": "Alto | Medio | Basso",
  "impact_color": "Rosso | Giallo | Verde",
  "thematic_area": "...",
  "document_cluster": "...",
  "summary": "...",
  "key_obligations": ["...", "..."],
  "target_functions": ["...", "..."],
  "suggested_action": "...",
  "confidence": "Alta | Media | Bassa",
  "status": "ANALYZED",
  "pdf_path": "{pdf_path}",
  "source_url": "{source_url}"
}}

NON usare markdown.
Restituisci solo JSON valido.
"""

@mcp.prompt()
def spiega_impatto(title: str, impact_level: str, reasoning: str) -> str:
    """Prompt utente per spiegare una classificazione di impatto."""
    return (
        "Spiega in modo semplice perché la seguente pubblicazione EBA è stata "
        f"classificata come impatto {impact_level}.\n\n"
        f"Titolo: {title}\n"
        f"Motivazione tecnica: {reasoning}\n\n"
        "Produci una spiegazione breve, comprensibile per un analista junior."
    )

