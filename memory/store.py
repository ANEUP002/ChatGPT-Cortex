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
# memory/store.py

from datetime import datetime
from typing import Optional


def prepare_memory_for_storage(
    summary: str,
    session_id: Optional[str] = None,
    memory_type: str = "conversation"
) -> dict:
    """
    Prepare a summary for storage by adding metadata.
    
    Args:
        summary: The text summary to store
        session_id: Optional session identifier
        memory_type: Type of memory (default: "conversation")
        
    Returns:
        Dictionary with text and metadata ready for Person 3's database
    """
    
    metadata = {
        "timestamp": datetime.now().isoformat(),
        "memory_type": memory_type
    }
    
    if session_id:
        metadata["session_id"] = session_id
    
    return {
        "text": summary,
        "metadata": metadata
    }


def store_memory(summary: str, vector_store, session_id: Optional[str] = None):
    """
    Store a memory summary in the database.
    
    Args:
        summary: The text summary to store
        vector_store: Person 3's vector database
        session_id: Optional session identifier
    """
    
    # Prepare the data
    memory_data = prepare_memory_for_storage(summary, session_id)
    
    # Call Person 3's storage function
    # (This interface will be confirmed with Person 3 on Day 3)
    try:
        vector_store.add(
            text=memory_data["text"],
            metadata=memory_data["metadata"]
        )
        print(f"Memory stored successfully: {summary[:50]}...")
    except Exception as e:
        print(f"Error storing memory: {e}")


# Test function
if __name__ == "__main__":
    test_summary = "User's name is Alice. User lives in Seattle."
    
    data = prepare_memory_for_storage(test_summary, session_id="test-123")
    
    print("Prepared memory data:")
    print(data)
