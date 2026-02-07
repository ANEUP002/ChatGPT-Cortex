"""
Chat Service Layer
Connects FastAPI to the LangGraph memory system
"""

import logging
from typing import Optional

from graph.pipeline import build_graph

logger = logging.getLogger(__name__)


class ChatService:
    """
    Service layer for chat processing.
    Delegates all intelligence + memory to LangGraph.
    """

    def __init__(self):
        # Build LangGraph once (expensive ops happen here, not per request)
        self.graph = build_graph()
        logger.info("LangGraph memory pipeline initialized")

    async def process_message(self, message: str, user_id: str) -> str:
        """
        Process incoming message through LangGraph memory system.
        """
        try:
            # Invoke the graph with the correct state shape
            final_state = self.graph.invoke({
                "user_input": message,
                "retrieved_memories": [],
                "response": None,
                "summary": None,
                "metadata": {
                    "session_id": user_id,
                    "timestamps": {},
                },
            })

            response = final_state.get("response")

            if not response:
                logger.warning("Graph returned no response")
                return "Sorry, I couldn't generate a response."

            return response

        except Exception as e:
            logger.exception("Error processing message via LangGraph")
            return f"Internal error: {str(e)}"
