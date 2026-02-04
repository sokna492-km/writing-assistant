from typing import List

import chromadb
from chromadb.config import Settings

from app.config import settings
from app.schemas import DraftChunk


class RagStore:
    def __init__(self) -> None:
        client = chromadb.PersistentClient(
            path=settings.chroma_path,
            settings=Settings(allow_reset=True),
        )
        self._collection = client.get_or_create_collection("thesis_memory")

    def ingest_draft(self, draft: DraftChunk) -> None:
        self._collection.add(
            ids=[draft.id],
            documents=[draft.content],
            metadatas=[draft.metadata],
        )

    def ingest_pdf(self, pdf_url: str, notes: str | None) -> None:
        self._collection.add(
            ids=[f"pdf:{pdf_url}"],
            documents=[notes or "PDF reference"],
            metadatas=[{"pdf_url": pdf_url}],
        )

    def search(self, query: str, top_k: int) -> List[str]:
        results = self._collection.query(query_texts=[query], n_results=top_k)
        return results.get("documents", [[]])[0]
