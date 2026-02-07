"""
Embedding configuration for the project.
Everyone imports from here - don't create embeddings elsewhere.
"""

from langchain_openai import OpenAIEmbeddings


def get_embeddings():
    """Returns the embedding model. Change here to swap models."""
    return OpenAIEmbeddings(model="text-embedding-3-small")
