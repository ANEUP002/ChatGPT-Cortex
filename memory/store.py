"""
Storage boundary between LangGraph and the vector database.
Accepts summaries, stores them. No summarization or retrieval logic here.
"""

from datetime import datetime
from typing import Optional
import uuid

from db.vector_store import add_documents


def store_summary(summary: str, metadata: Optional[dict] = None, session_id: Optional[str] = None) -> str:
    """Store a conversation summary. Returns the document ID."""
    meta = {
        "type": "summary",
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id or str(uuid.uuid4())
    }
    
    if metadata:
        meta.update(metadata)
    
    ids = add_documents([summary], [meta])
    return ids[0] if ids else ""


def store_memory(session_id: str, summary: str, metadata: Optional[dict] = None) -> str:
    """
    Alias for store_summary - matches the interface expected by graph/pipeline.py
    """
    return store_summary(summary=summary, metadata=metadata, session_id=session_id)
