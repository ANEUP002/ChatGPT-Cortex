# prompts/__init__.py

from .summary_prompts import get_summary_prompt, SUMMARIZATION_PROMPT
from .system_prompts import get_system_prompt, SYSTEM_PROMPT_WITH_MEMORY, SYSTEM_PROMPT_NO_MEMORY

__all__ = [
    "get_summary_prompt",
    "SUMMARIZATION_PROMPT",
    "get_system_prompt",
    "SYSTEM_PROMPT_WITH_MEMORY",
    "SYSTEM_PROMPT_NO_MEMORY"
]