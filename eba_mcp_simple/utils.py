
# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================
# Questo modulo contiene:
# - helper testuali;
# - gestione URL;
# - gestione repository locale;
# - salvataggio/caricamento JSON.
# =============================================================================

from __future__ import annotations

import json
import re
from urllib.parse import urljoin

from fastmcp.exceptions import ToolError

from eba_mcp_simple.config import (
    EBA_BASE_URL,
    METADATA_DIR,
    PDF_DIR,
    METADATA_FILE,
    ASSESSMENTS_FILE,
)

from eba_mcp_simple.models import (
    EbaPublication,
    GuidelineAssessment,
)


def clean_text(value: str | None) -> str:
    return " ".join((value or "").split())


def make_absolute_url(href: str) -> str:
    return urljoin(EBA_BASE_URL, href)

def ensure_repository() -> None:
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    PDF_DIR.mkdir(parents=True, exist_ok=True)


def save_publications_metadata(publications: list[EbaPublication]) -> None:
    ensure_repository()
    data = [pub.model_dump() for pub in publications]
    METADATA_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

def save_assessments(
    assessments: list[GuidelineAssessment],
) -> None:
    ensure_repository()

    data = [item.model_dump() for item in assessments]

    ASSESSMENTS_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

def load_assessments() -> list[GuidelineAssessment]:
    if not ASSESSMENTS_FILE.exists():
        return []

    data = json.loads(
        ASSESSMENTS_FILE.read_text(encoding="utf-8")
    )

    return [GuidelineAssessment(**item) for item in data]


def load_publications_metadata() -> list[EbaPublication]:
    if not METADATA_FILE.exists():
        raise ToolError(
            "Nessuna pubblicazione storicizzata trovata. "
            "Esegui prima il tool `fetch_eba_publications` per recuperare e salvare le ultime Guidelines EBA."
        )

    data = json.loads(METADATA_FILE.read_text(encoding="utf-8"))
    return [EbaPublication(**item) for item in data]


def safe_filename(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")[:120]

