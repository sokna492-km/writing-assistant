from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class Mode(str, Enum):
    socratic = "socratic"
    review = "review"
    structure = "structure"
    default = "default"


class AgentRole(str, Enum):
    research = "research"
    critic = "critic"
    synthesizer = "synthesizer"


class Citation(BaseModel):
    title: str
    authors: List[str]
    year: int
    doi: Optional[str] = None
    url: Optional[HttpUrl] = None
    source: Optional[str] = None


class ResearchQuery(BaseModel):
    query: str
    filters: Optional[dict] = None


class DraftChunk(BaseModel):
    id: str
    content: str
    metadata: dict = Field(default_factory=dict)


class RagIngestRequest(BaseModel):
    draft: Optional[DraftChunk] = None
    pdf_url: Optional[HttpUrl] = None
    notes: Optional[str] = None


class RagSearchRequest(BaseModel):
    query: str
    top_k: int = 5


class AgentRequest(BaseModel):
    prompt: str
    mode: Mode = Mode.default
    citations: List[Citation] = Field(default_factory=list)
    memory_context: Optional[str] = None


class AgentResponse(BaseModel):
    mode: Mode
    research: Optional[str] = None
    critic: Optional[str] = None
    synthesizer: Optional[str] = None
    challenge_questions: List[str] = Field(default_factory=list)
    citations: List[Citation] = Field(default_factory=list)


class CitationFormatRequest(BaseModel):
    citations: List[Citation]


class CitationFormatResponse(BaseModel):
    apa: List[str]
