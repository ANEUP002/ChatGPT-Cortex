"""
Memory retrieval module.
Finds relevant past memories for the current question.
"""

from typing import List, Optional

from db.vector_store import similarity_search


def retrieve_memories(query: str, session_id: Optional[str] = None, k: int = 3) -> List[dict]:
    """
    Find the most relevant past memories for the current question.
    
    Args:
        query: Current user message
        session_id: Optional session filter (not used yet)
        k: How many memories to retrieve (default: 3)
        
    Returns:
        List of memory dicts with text and metadata
    """
    try:
        results = similarity_search(query, k=k)
        
        # Convert Document objects to dicts
        memories = []
        for doc in results:
            memories.append({
                "text": doc.page_content,
                "metadata": doc.metadata
            })
        
        return memories
        
    except Exception as e:
        print(f"Error retrieving memories: {e}")
        return []


def retrieve_relevant_memories(user_input: str, vector_store=None, k: int = 3, metadata_filter: Optional[dict] = None) -> List[str]:
    """
    Legacy interface - returns just the text strings.
    """
    memories = retrieve_memories(user_input, k=k)
    return [m["text"] for m in memories]


def format_memories_for_prompt(memories: List[str]) -> str:
    """Format retrieved memories into a text block for the LLM."""
    if not memories:
        return "No relevant past memories."
    
    formatted = "=== Relevant Past Information ===\n"
    for i, memory in enumerate(memories, 1):
        formatted += f"{i}. {memory}\n"
    formatted += "================================\n"
    
    return formatted