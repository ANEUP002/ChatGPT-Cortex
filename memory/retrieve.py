# memory/retrieve.py

from typing import List, Optional


def retrieve_relevant_memories(
    user_input: str,
    vector_store,  # This will come from Person 3
    k: int = 3,
    metadata_filter: Optional[dict] = None
) -> List[str]:
    """
    Find the most relevant past memories for the current question.
    
    Args:
        user_input: Current user message
        vector_store: The database (Person 3 provides this)
        k: How many memories to retrieve (default: 3)
        metadata_filter: Optional filters (e.g., session_id)
        
    Returns:
        List of memory strings, most relevant first
    """
    
    try:
        # This is how you'll call Person 3's code
        results = vector_store.search(
            query=user_input,
            k=k,
            filter=metadata_filter
        )
        
        # Extract just the text from results
        memories = [result["text"] for result in results]
        
        return memories
        
    except Exception as e:
        print(f"Error retrieving memories: {e}")
        return []  # Return empty list if retrieval fails


def format_memories_for_prompt(memories: List[str]) -> str:
    """
    Format retrieved memories into a nice text block for the LLM.
    
    Args:
        memories: List of memory strings
        
    Returns:
        Formatted string ready to inject into LLM prompt
    """
    
    if not memories:
        return "No relevant past memories."
    
    formatted = "=== Relevant Past Information ===\n"
    for i, memory in enumerate(memories, 1):
        formatted += f"{i}. {memory}\n"
    formatted += "================================\n"
    
    return formatted


# Test function
if __name__ == "__main__":
    # Mock test without real database
    print("Testing memory formatting...")
    
    fake_memories = [
        "User's name is Alice.",
        "User's favorite color is blue.",
        "User lives in Seattle."
    ]
    
    formatted = format_memories_for_prompt(fake_memories)
    print(formatted)