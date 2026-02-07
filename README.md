# ChatGPT-Cortex

Persistent Memory for ChatGPT using LangGraph + Vector Retrieval

## Project Structure

```
├── api/           # REST API endpoints (Person 4)
├── db/            # Storage infrastructure (Person 3)
│   ├── embeddings.py    # Embedding model config
│   └── vector_store.py  # Chroma database interface
├── eval/          # Evaluation scripts (Person 4)
├── graph/         # LangGraph orchestration (Person 1)
├── memory/        # Memory logic & storage
│   └── store.py         # Storage boundary (Person 3)
├── prompts/       # Prompt templates
└── tests/         # Test suite
```

## Quick Start

```bash
pip install -r requirements.txt
```

## Storage Layer (Implemented)

```python
# Store a memory
from memory.store import store_summary
store_summary("User prefers Python", session_id="abc123")

# Search memories
from db.vector_store import similarity_search
results = similarity_search("programming languages")
```

## Team Ownership

| Role | Owns | Responsibility |
|------|------|----------------|
| Person 1 | `graph/` | LangGraph orchestration |
| Person 2 | `memory/` (logic) | Summarization & retrieval |
| Person 3 | `db/`, `memory/store.py` | Storage infrastructure |
| Person 4 | `api/`, `eval/` | API & evaluation |
