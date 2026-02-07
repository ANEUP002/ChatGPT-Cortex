"""
Chat Service Layer
Handles business logic for processing messages
For now, this is a simple implementation that will connect to the graph later
"""

import os
from typing import Optional
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)


class ChatService:
    """
    Service layer for chat processing
    Currently uses basic OpenAI API
    Will be upgraded to use LangGraph memory system once teammates complete their parts
    """
    
    def __init__(self):
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not found in environment")
        
        self.client = OpenAI(api_key=api_key) if api_key else None
        
        # This will later be replaced with the graph from Person 1
        self.memory_graph = None
        
    async def process_message(self, message: str, user_id: str) -> str:
        """
        Process incoming message and generate response
        
        TODO: Connect to LangGraph memory system once Person 1 completes graph/
        For now, uses basic OpenAI API
        """
        
        # Placeholder: Will call memory graph here
        # response = self.memory_graph.invoke({"message": message, "user_id": user_id})
        
        if not self.client:
            return "Error: OpenAI API key not configured. Please add OPENAI_API_KEY to .env file"
        
        try:
            # Simple chat completion (no memory yet)
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message}
                ]
            )
            
            response = completion.choices[0].message.content
            logger.info(f"Generated response for user {user_id}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}")
            return f"Error generating response: {str(e)}"
    
    def connect_graph(self, graph):
        """
        Connect to the LangGraph memory system
        This will be called once Person 1 completes the graph
        """
        self.memory_graph = graph
        logger.info("Memory graph connected to service")