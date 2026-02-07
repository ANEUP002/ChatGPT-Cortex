"""
Chat Service Layer
Connects the API to the LangGraph memory pipeline.
"""

import os
import uuid
from dotenv import load_dotenv
load_dotenv()

from typing import Optional
import logging

from graph.pipeline import build_graph

logger = logging.getLogger(__name__)


class ChatService:
    """Service layer that uses the LangGraph memory pipeline."""
    
    def __init__(self):
        # Build the memory graph
        try:
            self.memory_graph = build_graph()
            logger.info("Memory graph initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize memory graph: {e}")
            self.memory_graph = None
        
    async def process_message(self, message: str, user_id: str) -> str:
        """Process message through the memory pipeline."""
        
        if not self.memory_graph:
            return "Error: Memory system not initialized"
        
        try:
            # Build initial state
            initial_state = {
                "user_input": message,
                "retrieved_memories": [],
                "response": "",
                "summary": None,
                "metadata": {
                    "session_id": user_id,
                    "timestamps": {}
                }
            }
            
            # Run through the graph
            result = self.memory_graph.invoke(initial_state)
            
            response = result.get("response", "No response generated")
            logger.info(f"Generated response for user {user_id}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error in memory pipeline: {str(e)}")
            return f"Error: {str(e)}"