"""
Vector database interface using Chroma.
Handles storing and searching memory summaries.
"""

import os
from datetime import datetime
from typing import Optional

from langchain_chroma import Chroma
from langchain_core.documents import Document

from db.embeddings import get_embeddings


CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
_vector_store: Optional[Chroma] = None


def init_vector_store(persist_directory: str = CHROMA_PERSIST_DIR) -> Chroma:
    """Initialize or return existing store. Data persists to ./chroma_db/"""
    global _vector_store
    
    if _vector_store is not None:
        return _vector_store
    
    os.makedirs(persist_directory, exist_ok=True)
    
    _vector_store = Chroma(
        collection_name="gpt_memory",
        embedding_function=get_embeddings(),
        persist_directory=persist_directory
    )
    
    return _vector_store


def add_documents(texts: list[str], metadata: list[dict]) -> list[str]:
    """Store text with metadata. Returns list of doc IDs."""
    store = init_vector_store()
    
    documents = []
    for text, meta in zip(texts, metadata):
        if "timestamp" not in meta:
            meta["timestamp"] = datetime.now().isoformat()
        documents.append(Document(page_content=text, metadata=meta))
    
    return store.add_documents(documents)


def similarity_search(query: str, k: int = 5) -> list[Document]:
    """Find k most similar documents to query."""
    store = init_vector_store()
    return store.similarity_search(query, k=k)


def persist():
    """Explicit save. Chroma auto-saves but keeping for FAISS compat."""
    pass
