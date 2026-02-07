# memory/summarize.py

from openai import OpenAI
from prompts.summary_prompts import get_summary_prompt

client = OpenAI()  # You'll need OPENAI_API_KEY in environment


def summarize_conversation(user_input: str, assistant_response: str) -> str:
    """
    Take a conversation turn and create a short, factual summary.
    
    Args:
        user_input: What the user said
        assistant_response: What the AI replied
        
    Returns:
        A 3-5 line summary of important facts/preferences
        
    Example:
        user: "My name is Alice and I love pizza"
        assistant: "Nice to meet you Alice! Pizza is great."
        → summary: "User's name is Alice. User enjoys pizza."
    """
    
    # Get the prompt from our prompts module
    prompt = get_summary_prompt(user_input, assistant_response)
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,  # Low temperature for consistent summaries
        max_tokens=150
    )
    
    summary = response.choices[0].message.content.strip()
    return summary


# Test function
if __name__ == "__main__":
    # Test case
    test_user = "My favorite color is blue and I live in Seattle"
    test_assistant = "That's great! Blue is a calming color."
    
    result = summarize_conversation(test_user, test_assistant)
    print("Summary:")
    print(result)