# prompts/system_prompts.py

SYSTEM_PROMPT_WITH_MEMORY = """
You are a helpful AI assistant with access to memories from past conversations.

Below are relevant facts and context from previous interactions:

{retrieved_memories}

Use this information to provide personalized and contextually aware responses.
If the memories contain relevant information, incorporate it naturally into your answer.
If the memories don't help with the current question, just answer normally.

Current user message: {user_input}
"""


SYSTEM_PROMPT_NO_MEMORY = """
You are a helpful AI assistant.

Current user message: {user_input}
"""


def get_system_prompt(user_input: str, retrieved_memories: str = None) -> str:
    """
    Get the appropriate system prompt based on whether we have memories.
    
    Args:
        user_input: Current user message
        retrieved_memories: Formatted string of past memories (optional)
        
    Returns:
        Complete system prompt
    """
    if retrieved_memories:
        return SYSTEM_PROMPT_WITH_MEMORY.format(
            retrieved_memories=retrieved_memories,
            user_input=user_input
        )
    else:
        return SYSTEM_PROMPT_NO_MEMORY.format(user_input=user_input)


# Test function
if __name__ == "__main__":
    # Test without memories
    prompt1 = get_system_prompt("What's my favorite color?")
    print("=== NO MEMORY ===")
    print(prompt1)
    print()
    
    # Test with memories
    memories = "User's name is Alice.\nUser's favorite color is blue."
    prompt2 = get_system_prompt("What's my favorite color?", memories)
    print("=== WITH MEMORY ===")
    print(prompt2)