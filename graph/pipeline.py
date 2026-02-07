"""
LangGraph pipeline for memory-augmented chat.
Orchestrates: ingest → retrieve → generate → summarize → store
"""

import os
from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END
from datetime import datetime
from openai import OpenAI

from graph.state import MemoryState
from memory.store import store_memory
from memory.retrieve import retrieve_memories, format_memories_for_prompt
from prompts.system_prompts import get_system_prompt
from prompts.summary_prompts import get_summary_prompt

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ingest_input(state: MemoryState):
    """Entry node - stamps metadata with timestamp."""
    return {
        "metadata": {
            **state["metadata"],
            "timestamps": {
                **state["metadata"].get("timestamps", {}),
                "ingest_input": datetime.utcnow().isoformat(),
            },
        }
    }


def retrieve_memory(state: MemoryState):
    """Retrieves memories relevant to the current user input."""
    memories = retrieve_memories(
        query=state["user_input"],
        session_id=state["metadata"].get("session_id"),
    )
    return {"retrieved_memories": memories}


def generate_response(state: MemoryState):
    """Generates the assistant response using OpenAI with retrieved memories."""
    user_input = state["user_input"]
    memories = state.get("retrieved_memories", [])
    
    # Format memories for the prompt
    memory_texts = [m["text"] for m in memories] if memories else []
    formatted_memories = format_memories_for_prompt(memory_texts) if memory_texts else None
    
    # Build system prompt with memories
    system_prompt = get_system_prompt(user_input, formatted_memories)
    
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        response = completion.choices[0].message.content
    except Exception as e:
        response = f"Error generating response: {str(e)}"
    
    return {"response": response}


def summarize_interaction(state: MemoryState):
    """Produces a compact summary suitable for long-term memory."""
    user_input = state["user_input"]
    response = state.get("response", "")
    
    try:
        prompt = get_summary_prompt(user_input, response)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=150
        )
        summary = completion.choices[0].message.content.strip()
    except Exception as e:
        summary = f"User said: {user_input}"
    
    return {"summary": summary}


def store_memory_node(state: MemoryState):
    """Single, explicit memory persistence point."""
    summary = state.get("summary")
    session_id = state["metadata"].get("session_id")

    if not summary or not session_id:
        return {}

    store_memory(
        session_id=session_id,
        summary=summary,
        metadata=state["metadata"],
    )

    return {}


def build_graph():
    """Build and compile the LangGraph state machine."""
    graph = StateGraph(MemoryState)

    graph.add_node("ingest_input", ingest_input)
    graph.add_node("retrieve_memory", retrieve_memory)
    graph.add_node("generate_response", generate_response)
    graph.add_node("summarize_interaction", summarize_interaction)
    graph.add_node("store_memory", store_memory_node)

    graph.set_entry_point("ingest_input")

    graph.add_edge("ingest_input", "retrieve_memory")
    graph.add_edge("retrieve_memory", "generate_response")
    graph.add_edge("generate_response", "summarize_interaction")
    graph.add_edge("summarize_interaction", "store_memory")
    graph.add_edge("store_memory", END)

    return graph.compile()