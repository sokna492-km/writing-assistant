from typing import List

from fastapi import APIRouter, Depends, Header, HTTPException

from app.agents.orchestrator import AssistantOrchestrator
from app.rag.store import RagStore
from app.schemas import (
    AgentRequest,
    AgentResponse,
    Citation,
    CitationFormatRequest,
    CitationFormatResponse,
    RagIngestRequest,
    RagSearchRequest,
)

router = APIRouter()


def _get_user(authorization: str | None = Header(default=None)) -> str:
    if authorization is None:
        return "anonymous"
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    return "firebase-user"


def _format_apa(citation: Citation) -> str:
    author_str = "; ".join(citation.authors)
    doi_or_url = citation.doi or (citation.url if citation.url else "")
    source = f" {citation.source}." if citation.source else ""
    return f"{author_str} ({citation.year}). {citation.title}.{source} {doi_or_url}".strip()


@router.post("/agents/run", response_model=AgentResponse)
def run_agents(request: AgentRequest, user_id: str = Depends(_get_user)) -> AgentResponse:
    orchestrator = AssistantOrchestrator()
    response = orchestrator.run(request)
    return response


@router.post("/rag/ingest")
def rag_ingest(request: RagIngestRequest, user_id: str = Depends(_get_user)) -> dict:
    store = RagStore()
    if request.draft:
        store.ingest_draft(request.draft)
    if request.pdf_url:
        store.ingest_pdf(str(request.pdf_url), request.notes)
    return {"status": "ok"}


@router.post("/rag/search")
def rag_search(request: RagSearchRequest, user_id: str = Depends(_get_user)) -> dict:
    store = RagStore()
    results = store.search(request.query, request.top_k)
    return {"results": results}


@router.post("/citations/format", response_model=CitationFormatResponse)
def format_citations(
    request: CitationFormatRequest, user_id: str = Depends(_get_user)
) -> CitationFormatResponse:
    apa_list = [_format_apa(citation) for citation in request.citations]
    return CitationFormatResponse(apa=apa_list)
