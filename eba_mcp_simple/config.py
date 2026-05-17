
# =============================================================================
# CONFIGURAZIONE
# =============================================================================
#
# Questo modulo definisce la parametrizzazione necessaria nei programmi successivi
#
# =============================================================================





from pathlib import Path

EBA_BASE_URL = "https://www.eba.europa.eu"
EBA_PUBLICATIONS_URL = (
    "https://www.eba.europa.eu/publications-and-media/publications"
    "?text=&document_type=250&media_topics=All"
)

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; EBA-MCP-Scraper/1.0)"
}
REPOSITORY_DIR = Path("repository")
METADATA_DIR = REPOSITORY_DIR / "metadata"
PDF_DIR = REPOSITORY_DIR / "pdf"
METADATA_FILE = METADATA_DIR / "eba_publications.json"
ASSESSMENTS_FILE = METADATA_DIR / "assessments.json"
