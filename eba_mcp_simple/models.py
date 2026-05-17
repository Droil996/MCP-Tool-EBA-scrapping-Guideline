
from typing import Literal
from pydantic import BaseModel

# =============================================================================
# MODELS
# =============================================================================
# Questo modulo contiene i modelli Pydantic impiegati 
#
# - EBA Publication
# - PDF Download Result
# - GuidelineAssessment
# - PdfPreview
#
# =============================================================================


class EbaPublication(BaseModel):
    title: str
    url: str
    download_url: str = ""
    description: str = ""
    document_type: str = "unknown"


class PdfDownloadResult(BaseModel):
    title: str
    source_url: str
    saved_path: str
    status: str

class GuidelineAssessment(BaseModel):
    title: str
    relevance_score: Literal["Alto", "Medio", "Basso"]
    impact_color: Literal["Rosso", "Giallo", "Verde"]
    thematic_area: str
    document_cluster: str
    summary: str
    key_obligations: list[str]
    target_functions: list[str]
    suggested_action: str
    confidence: Literal["Alta", "Media", "Bassa"]
    status: str = "ANALYZED"
    pdf_path: str = ""
    source_url: str = ""

class PdfPreview(BaseModel):
    title: str
    pdf_path: str
    page_count: int
    preview_text: str

