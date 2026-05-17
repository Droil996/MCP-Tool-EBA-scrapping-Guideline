from __future__ import annotations

import requests

from bs4 import BeautifulSoup
from fastmcp.exceptions import ToolError
from pypdf import PdfReader

from eba_mcp_simple.mcp_instance import mcp

from eba_mcp_simple.config import (
    EBA_PUBLICATIONS_URL,
    REQUEST_HEADERS,
    PDF_DIR,
)

from eba_mcp_simple.models import (
    EbaPublication,
    PdfDownloadResult,
    PdfPreview,
    GuidelineAssessment,
)

from eba_mcp_simple.utils import (
    clean_text,
    make_absolute_url,
    ensure_repository,
    save_publications_metadata,
    save_assessments,
    load_assessments,
    load_publications_metadata,
    safe_filename,
)

# =============================================================================
# MCP TOOLS
# =============================================================================
# Questo modulo contiene tutti i tool MCP esposti dal server:
#
# - fetch pubblicazioni EBA
# - download PDF
# - estrazione preview PDF
# - salvataggio assessment 
#
# =============================================================================


# =============================================================================
# FETCH TOOLS
# =============================================================================

@mcp.tool(annotations={"readOnlyHint": True})
def fetch_eba_publications(max_results: int = 5) -> list[EbaPublication]:
    """Recupera pubblicazioni EBA reali dalla pagina ufficiale.

    Cerca solo i link 'Download document', evitando menu, navbar e footer.
    """
    if not 1 <= max_results <= 20:
        raise ToolError("max_results deve essere tra 1 e 20")

    try:
        response = requests.get(
            EBA_PUBLICATIONS_URL,
            timeout=15,
            headers=REQUEST_HEADERS,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ToolError(f"Errore durante il download della pagina EBA: {exc}") from exc

    soup = BeautifulSoup(response.text, "html.parser")
    publications: list[EbaPublication] = []
    seen_urls: set[str] = set()

    for link in soup.find_all("a", href=True):
        link_text = clean_text(link.get_text(" ", strip=True))

        if link_text != "Download document":
            continue

        download_url = make_absolute_url(link["href"])

        if download_url in seen_urls:
            continue

        title_tag = link.find_previous("h4")
        if title_tag is None:
            continue

        title = clean_text(title_tag.get_text(" ", strip=True))
        if not title:
            continue

        title_link = title_tag.find("a", href=True)
        publication_url = (
            make_absolute_url(title_link["href"])
            if title_link
            else download_url
        )

        publications.append(
            EbaPublication(
                title=title,
                url=publication_url,
                download_url=download_url,
                description="",
                document_type="Guidelines",
            )
        )

        seen_urls.add(download_url)

        if len(publications) >= max_results:
            break

    if not publications:
        raise ToolError(
            "Nessuna pubblicazione trovata nella pagina EBA. "
            "La struttura HTML potrebbe essere cambiata."
        )
    save_publications_metadata(publications)
    return publications

# =============================================================================
# PDF TOOLS
# =============================================================================

@mcp.tool()
def download_eba_pdfs(limit: int = 3) -> list[PdfDownloadResult]:
    """Scarica i PDF delle pubblicazioni EBA già storicizzate."""

    if not 1 <= limit <= 20:
        raise ToolError("limit deve essere tra 1 e 20")

    publications = load_publications_metadata()
    ensure_repository()

    results: list[PdfDownloadResult] = []

    for pub in publications[:limit]:

        if not pub.download_url:
            results.append(
                PdfDownloadResult(
                    title=pub.title,
                    source_url="",
                    saved_path="",
                    status="SKIPPED: download_url mancante",
                )
            )
            continue

        filename = safe_filename(pub.title) + ".pdf"
        output_path = PDF_DIR / filename

        if output_path.exists():
            results.append(
                PdfDownloadResult(
                    title=pub.title,
                    source_url=pub.download_url,
                    saved_path=str(output_path),
                    status="ALREADY_EXISTS",
                )
            )
            continue

        try:
            response = requests.get(
                pub.download_url,
                timeout=30,
                headers=REQUEST_HEADERS,
            )

            response.raise_for_status()

            content_type = response.headers.get(
                "Content-Type",
                "",
            ).lower()

            if (
                "pdf" not in content_type
                and not pub.download_url.lower().endswith(".pdf")
            ):
                results.append(
                    PdfDownloadResult(
                        title=pub.title,
                        source_url=pub.download_url,
                        saved_path="",
                        status=f"SKIPPED: il link non sembra un PDF diretto ({content_type})",
                    )
                )
                continue

            output_path.write_bytes(response.content)

            results.append(
                PdfDownloadResult(
                    title=pub.title,
                    source_url=pub.download_url,
                    saved_path=str(output_path),
                    status="DOWNLOADED",
                )
            )

        except requests.RequestException as exc:
            results.append(
                PdfDownloadResult(
                    title=pub.title,
                    source_url=pub.download_url,
                    saved_path="",
                    status=f"ERROR: {exc}",
                )
            )

    return results

@mcp.tool(annotations={"readOnlyHint": True})
def extract_pdf_preview(
    limit: int = 3,
    max_pages: int = 3,
) -> list[PdfPreview]:
    """Estrae una preview testuale dai PDF scaricati."""

    if not 1 <= limit <= 20:
        raise ToolError("limit deve essere tra 1 e 20")

    if not 1 <= max_pages <= 10:
        raise ToolError("max_pages deve essere tra 1 e 10")

    ensure_repository()

    pdf_files = list(PDF_DIR.glob("*.pdf"))

    if not pdf_files:
        raise ToolError(
            "Nessun PDF trovato. "
            "Esegui prima download_eba_pdfs."
        )

    previews: list[PdfPreview] = []

    for pdf_path in pdf_files[:limit]:

        try:
            reader = PdfReader(str(pdf_path))
            page_count = len(reader.pages)

            texts: list[str] = []

            for page in reader.pages[:max_pages]:
                text = page.extract_text() or ""

                if text.strip():
                    texts.append(text.strip())

            preview_text = "\n\n".join(texts)
            preview_text = preview_text[:6000]

            previews.append(
                PdfPreview(
                    title=pdf_path.stem.replace("_", " ").title(),
                    pdf_path=str(pdf_path),
                    page_count=page_count,
                    preview_text=preview_text,
                )
            )

        except Exception as exc:
            raise ToolError(
                f"Errore lettura PDF {pdf_path}: {exc}"
            ) from exc

    return previews


# =============================================================================
# ASSESSMENT TOOLS
# =============================================================================

@mcp.tool()
def save_guideline_assessment(
    assessment: GuidelineAssessment,
) -> str:
    """Salva assessment prodotto dall'Agent."""

    assessments = load_assessments()

    assessments = [
        item
        for item in assessments
        if item.title != assessment.title
    ]

    assessments.append(assessment)

    save_assessments(assessments)

    return f"Assessment salvato per: {assessment.title}"


@mcp.tool(annotations={"readOnlyHint": True})
def get_guideline_assessments() -> list[GuidelineAssessment]:
    """Restituisce tutte le valutazioni regolamentari salvate."""
    return load_assessments()
