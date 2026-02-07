from langgraph.graph import StateGraph, END
from datetime import datetime

from graph.state import MemoryState
from memory.store import retrieve_memories, store_memory

def ingest_input(state: MemoryState):
    """
    Entry Node which is responsible for stamping the metadata
    
    """
    return {
        "metadata":{
            **state["metadata"],
            "timestamps":{
                **state["metadata"].get("timestamps", {}),
                "ingest_input":datetime.utcnow().isoformat(),
            },
        }
    }
def retrieve_memory(state: MemoryState):
    """Retrieves memories relevant to the current user input
    Storage mechanism is opaque to this layer.
    """
    memories = retrieve_memories(
        session_id = state["metadata"]["session_id"],
        query=state["user_input"],
    )
    return {"retrieved_memories":memories}

def generate_response(state:MemoryState):
    """
    generates the assistant response.
    Actual LLM logic is intentionally abstracted
    """

    response = "This is a placeholder response."
    return {"response":response}


def summarize_interaction(state: MemoryState):
    """Produces a compactsummary suitable for long-term memory"""
    summary = f"User said:{state['user_input']}"
    return {"summary": summary}

def store_memory_node(state: MemoryState):
    """
    Single, explicit memory persistence point.
    Saving is conditional and auditable.
    """
    summary = state.get("summary")
    session_id = state["metadata"].get("session_id")

    # Explicit guard: no implicit saves
    if not summary or not session_id:
        return {}

    store_memory(
        session_id=session_id,
        summary=summary,
        metadata=state["metadata"],
    )

    return {}


###building the orchestration
def build_graph():
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