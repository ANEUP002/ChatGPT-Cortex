# prompts/summary_prompts.py

SUMMARIZATION_PROMPT = """
You are creating memory summaries for a conversational AI system.
Extract ONLY factual information, preferences, or constraints from this conversation.

User said: {user_input}
Assistant said: {assistant_response}

Create a 3-5 line summary focusing on:
- Facts about the user (name, location, job, etc.)
- User preferences (likes, dislikes, habits)
- Important context for future conversations
- Specific requests or constraints

Rules:
- Be concise and factual
- No opinions or commentary
- No filler words
- Focus on what's memorable and useful

Summary:
"""


def get_summary_prompt(user_input: str, assistant_response: str) -> str:
    """
    Format the summarization prompt with actual conversation content.
    
    Args:
        user_input: What the user said
        assistant_response: What the AI replied
        
    Returns:
        Formatted prompt ready to send to LLM
    """
    return SUMMARIZATION_PROMPT.format(
        user_input=user_input,
        assistant_response=assistant_response
    )


# Test function
if __name__ == "__main__":
    test_user = "My name is Alice and I love pizza"
    test_assistant = "Nice to meet you Alice! Pizza is great."
    
    prompt = get_summary_prompt(test_user, test_assistant)
    print(prompt)